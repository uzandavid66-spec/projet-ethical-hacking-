from pathlib import Path
import sys

DONNEES = Path(__file__).resolve().parent / "donnees_fictives"


def lire_et_lister():
    if DONNEES.is_symlink():
        raise ValueError("Le dossier de données fictives est un lien symbolique.")
    exemple = DONNEES / "bonjour.txt"
    if exemple.is_symlink() or not exemple.is_file():
        raise ValueError("bonjour.txt doit être un fichier ordinaire dans le dossier de données fictives.")

    fichiers = []
    for dossier, sous_dossiers, noms in DONNEES.walk(on_error=propager_erreur):
        sous_dossiers[:] = [nom for nom in sous_dossiers if not (dossier / nom).is_symlink()]
        for nom in noms:
            fichier = dossier / nom
            if not fichier.is_symlink() and fichier.is_file():
                fichiers.append(fichier.relative_to(DONNEES))
    return exemple.read_text(encoding="utf-8"), sorted(fichiers)


def propager_erreur(erreur):
    raise erreur


def main():
    try:
        contenu, fichiers = lire_et_lister()
    except (OSError, ValueError) as erreur:
        print(f"Lecture des données fictives impossible : {erreur}", file=sys.stderr)
        return 1

    print(contenu.rstrip())
    for fichier in fichiers:
        print(fichier.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Projet Ethical Hacking - Client/Serveur C2

## Équipe
- Ayman (Serveur)
- Esra (Client Windows)
- David (Client/Serveur de base, tests et documentation)

## Fonctionnalités réalisées (David)
- Serveur TCP écoutant sur `0.0.0.0` (toutes les interfaces réseau).
- Gestion des clients multiples via `threading` (Windows) et `os.fork` (Linux).
- Client qui récupère l'IP réelle de la machine (pas de localhost).
- Exécution de commandes à distance (Shell/PowerShell).
- Capture d'écran à distance (sauvegardée au format PNG sur le serveur).
- Récupération de la base SAM et ajout au registre (nécessite les droits admin sous Windows).

## Lancement
1. Lancer le serveur : `python src/c2/serveur.py`
2. Lancer le client : `python src/c2/client.py`

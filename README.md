# Projet Ethical Hacking

## Objectif

On réalise une démonstration client-serveur en Python pour comprendre
comment deux programmes communiquent avec des sockets TCP.

Les deux programmes tournent sur la même machine (`127.0.0.1`).
Le client envoie `Bonjour` et le serveur répond `OK`.

## Répartition du travail

| Membre | Travail prévu |
| --- | --- |
| Ayman — membre 1 | Écrire `serveur.py` et `client.py`, puis vérifier que les deux scripts communiquent. |
| Esra — membre 2 | Partie à confirmer avec le groupe. |
| David — membre 3 | Préparer les tests, noter les résultats et rédiger les instructions pour lancer la démo. |

## Tests prévus

- Serveur lancé : le client reçoit `OK`.
- Serveur arrêté : le client affiche un message clair.
- Depuis un clone propre : un membre du groupe suit le guide et reproduit la démo.

## Organisation sur GitHub

Ayman travaille sur `ayman-membre-1` et David sur `david-membre-3`.
Chacun pousse ses commits sur sa branche, puis ouvre une pull request
pour faire vérifier ses changements avant la fusion dans `main`.

Le guide de lancement sera complété après les premiers essais.
Les bonus seront ajoutés à partir de l’énoncé du TP.
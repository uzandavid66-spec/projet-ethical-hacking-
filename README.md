# Projet Ethical Hacking

## Objectif

Ce projet de groupe présente une démonstration de communication client-serveur en Python avec des sockets TCP. Les deux programmes s’exécutent sur la même machine, à l’adresse `127.0.0.1`. Le client envoie `Bonjour` et le serveur répond `OK`.

## Répartition du travail

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman — membre 1 | Développer `serveur.py` et `client.py`, puis vérifier l’échange entre les deux scripts. | `ayman-membre-1` |
| Esra — membre 2 | Contribution à préciser avec le groupe. | À définir |
| David — membre 3 | Écrire les tests du client et documenter le lancement de la démonstration. | `david-membre-3` |

## Lancer la démonstration

Une fois `serveur.py` et `client.py` réunis dans le dossier du projet, ouvrir deux terminaux dans VS Code.

Dans le premier terminal, lancer le serveur. Sous Windows, avec Python 3.14 installé :

```bat
py -3.14 serveur.py
```

Dans le deuxième terminal, lancer le client :

```bat
py -3.14 client.py
```

Le résultat attendu côté client est `Réponse du serveur : OK`. Relancer le serveur avant chaque nouvel essai.

## Lancer les tests du client

Depuis le dossier qui contient `client.py` et `test_client.py` :

```bat
py -3.14 -m unittest -v test_client
```

Les deux tests simulent une connexion. Le premier vérifie que le client envoie `Bonjour` et lit la réponse `OK`. Le second vérifie que la fonction du client signale un refus de connexion.

Les deux tests passent avec le client temporaire utilisé pendant le développement. Ils seront relancés avec le client d’Ayman, puis l’échange complet sera vérifié avec les deux scripts.

## Organisation sur GitHub

Chaque membre fait ses commits et ses pushs sur sa propre branche. Une pull request permet à un autre membre de relire les changements et de vérifier leur fonctionnement avant la fusion dans `main`.

## Bonus

Les bonus seront détaillés à partir de l’énoncé du TP.
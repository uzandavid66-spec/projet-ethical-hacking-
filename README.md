# Projet Ethical Hacking — Démonstration TCP locale

La démo de David montre un échange TCP entre deux programmes Python sur la même machine. Le client envoie `Bonjour` et reçoit `OK` sur `127.0.0.1:5000`. Ayman a également testé un échange avec son client de simulation sous Kali.

## Équipe

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman — membre 1 | Serveur TCP et client de simulation testés sous Kali. | `ayman-membre-1` |
| Esra — membre 2 | Contribution à confirmer avec le groupe. | À confirmer |
| David — membre 3 | Démonstration TCP sous Windows, tests unitaires et documentation. | `david-membre-3` |

## Lancer la démo sous Windows

Ouvrir deux terminaux dans VS Code à la racine du dépôt. Dans le premier, lancer le serveur.

```bat
py -3.14 src/c2/serveur_demo.py
```

Quand le serveur affiche `Serveur de test sur 127.0.0.1:5000`, lancer le client dans le second terminal.

```bat
py -3.14 src/c2/client_demo.py
```

Le client doit recevoir `OK`. Le serveur s’arrête après une connexion par défaut. Pour vérifier trois connexions successives, lancer le serveur avec `--clients 3`, puis lancer le client trois fois.

## Lancer les tests unitaires

Depuis la racine du dépôt, exécuter la commande suivante.

```bat
py -3.14 -m unittest -v test_client
```

Les deux tests utilisent `src/c2/client_demo.py`. Le premier vérifie l’envoi de `Bonjour` et la lecture de `OK`. Le second vérifie le refus de connexion. Les deux passent aussi depuis une copie du ZIP sans le `client.py` temporaire.

## Résultats

| Environnement | Vérification | Résultat |
| --- | --- | --- |
| Windows | Échange TCP local sur le port `5000` | Réponse `OK`, code de sortie `0` |
| Windows | Client lancé après l’arrêt du serveur | Connexion refusée, code de sortie `1` |
| Windows | Trois connexions successives | Trois réponses `OK`, puis arrêt du serveur |
| Kali | Connexion du client de simulation à `127.0.0.1:4444` | Connexion acceptée et processus fils créé |
| Kali | Aller-retour TCP avec le client de simulation | Le serveur affiche la réponse fictive du client |
| Kali | Transfert de données de test | Le serveur signale l’enregistrement des données reçues |

Pour le transfert sous Kali, `test.png` contenait du texte de test. La capture d’écran réelle reste à valider.

## Arborescence de la branche de David

```text
.
├── README.md
├── test_client.py
├── bin/
└── src/
    ├── c2/
    │   ├── client_demo.py
    │   └── serveur_demo.py
    ├── lin/
    └── win/
```

## Bonus du groupe de trois

Les bonus sont obligatoires pour le groupe. L’énoncé prévoit de les traiter après validation des fonctionnalités de base.

| Bonus | État |
| --- | --- |
| Chiffrement des communications | À faire |
| Chiffrement d’un dossier et export de la clé | À faire |
| Inventaire automatisé des services | À faire |
| Gestion de plusieurs clients | Trois connexions successives vérifiées sous Windows. Les connexions simultanées restent à vérifier. |

## Organisation et rendu

Chaque membre pousse ses changements sur sa branche. Le groupe relit les contributions dans des pull requests avant leur fusion dans `main`. Après validation, un membre du groupe dépose le ZIP complet du dépôt sur la plateforme.
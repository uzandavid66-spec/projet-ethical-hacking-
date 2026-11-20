# Projet Ethical Hacking — Démonstration TCP locale

La démonstration de David montre un échange TCP entre deux programmes Python sur la même machine. Le client envoie `Bonjour` et le serveur répond `OK` sur `127.0.0.1:5000`.

## Équipe

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman — membre 1 | Serveur socket et client de simulation testés pour la connexion sur Kali. | `ayman-membre-1` |
| Esra — membre 2 | Contribution à confirmer avec le groupe. | À confirmer |
| David — membre 3 | Démonstration TCP locale, tests du client et documentation. | `david-membre-3` |

## Lancer la démonstration sous Windows

Ouvrir deux terminaux dans VS Code à la racine du dépôt. Dans le premier, lancer le serveur de démonstration.

```bat
py -3.14 src/c2/serveur_demo.py
```

Quand le serveur affiche `Serveur de test sur 127.0.0.1:5000`, lancer le client dans le deuxième terminal.

```bat
py -3.14 src/c2/client_demo.py
```

Le client doit recevoir `OK`. Par défaut, le serveur s’arrête après une connexion. Pour vérifier trois connexions successives, lancer le serveur avec `--clients 3`, puis lancer le client trois fois.

## Lancer les tests unitaires

Depuis la racine du dépôt :

```bat
py -3.14 -m unittest -v test_client
```

Les tests simulent la connexion pour vérifier l’envoi de `Bonjour`, la lecture de `OK` et la gestion d’un refus de connexion.

## Résultats des vérifications

| Environnement | Vérification | Résultat |
| --- | --- | --- |
| Windows | Deux tests unitaires du client de David | 2 tests réussis |
| Windows | Échange TCP local sur le port `5000` | Réponse `OK`, code de sortie `0` |
| Windows | Client lancé après l’arrêt du serveur | Connexion refusée, code de sortie `1` |
| Windows | Trois connexions successives | Trois réponses `OK`, puis arrêt du serveur |
| Kali | Connexion du client de simulation d’Ayman sur `127.0.0.1:4444` | Connexion acceptée et processus fils créé |
| Kali | Réponse du client reçue par le serveur d’Ayman | À confirmer |

Le test sur Kali concerne `src/c2/main.py` et `tests/test_client.py` de la branche `ayman-membre-1`. Le serveur utilise `os.fork()` sous Linux. Les tests unitaires de David couvrent la démonstration Windows sur le port `5000`.

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

## Bonus demandés pour le groupe de trois

| Bonus | État |
| --- | --- |
| Chiffrement de la communication | À faire. Les messages de la démo TCP circulent en clair. |
| Chiffrement d’un dossier et export de la clé | À faire. |
| Inventaire automatisé des services | À faire. L’acceptation d’une simulation reste à confirmer avec le professeur. |
| Gestion de plusieurs clients | Trois connexions successives vérifiées sous Windows. La gestion simultanée reste à vérifier. |

## Organisation et rendu

Chaque membre pousse ses changements sur sa branche. Les contributions sont relues dans des pull requests avant leur fusion dans `main`. Après validation en groupe, un seul membre dépose le ZIP final sur la plateforme.
# Projet Ethical Hacking — Démonstration TCP

La démonstration de David utilise deux programmes Python qui communiquent en TCP sur `127.0.0.1:5000`. Le client envoie `Bonjour` et le serveur répond `OK`. Ayman a également réalisé un test avec son client de simulation sous Kali.

## Équipe

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman — membre 1 | Serveur TCP et client de simulation testés sous Kali | `ayman-membre-1` |
| Esra — membre 2 | Validation sous Windows proposée, à confirmer avec le groupe | À confirmer |
| David — membre 3 | Démonstration TCP sous Windows, tests unitaires, test d’intégration et documentation | `david-membre-3` |

## Lancer la démonstration sous Windows

Ouvrir deux terminaux à la racine du dépôt. Dans le premier, lancer le serveur.

```powershell
py -3.14 src/c2/serveur_demo.py
```

Attendre que le serveur affiche `Serveur de test sur 127.0.0.1:5000`, puis lancer le client dans le second terminal.

```powershell
py -3.14 src/c2/client_demo.py
```

Le client affiche `OK`. Par défaut, le serveur s’arrête après une connexion. Pour vérifier trois connexions successives, lancer le serveur avec `--clients 3`, puis lancer le client trois fois.

## Exécuter les tests

Depuis la racine du dépôt, lancer la commande suivante.

```powershell
py -3.14 -m unittest -v test_client test_tcp_integration
```

Les deux tests unitaires simulent la socket pour vérifier l’échange `Bonjour` → `OK` et le refus de connexion. Le test d’intégration ouvre une vraie connexion TCP locale sur un port libre et vérifie que le client reçoit `OK`. Il démarre son propre serveur de test.

**Résultat sous Windows avec Python 3.14.10** — `Ran 3 tests`, `OK`.

## Résultats des démonstrations

| Environnement | Vérification | Résultat |
| --- | --- | --- |
| Windows | Échange TCP local sur le port `5000` | Réponse `OK`, code de sortie `0` |
| Windows | Client lancé après l’arrêt du serveur | Connexion refusée, code de sortie `1` |
| Windows | Trois connexions successives | Trois réponses `OK`, puis arrêt du serveur |
| Kali | Connexion du client de simulation sur `127.0.0.1:4444` | Connexion acceptée et processus fils créé |
| Kali | Aller-retour TCP simulé | Le serveur affiche la réponse fictive reçue |
| Kali | Transfert de données de test | Le serveur signale l’enregistrement des données reçues |

Sous Kali, le fichier `test.png` contenait du texte de test. L’essai couvre le transfert de données. La capture d’écran réelle reste à valider.

## Arborescence de la branche de David

```text
.
├── README.md
├── test_client.py
├── test_tcp_integration.py
├── bin/
└── src/
    ├── c2/
    │   ├── client_demo.py
    │   └── serveur_demo.py
    ├── lin/
    └── win/
```

## Bonus du groupe de trois

L’énoncé rend les bonus obligatoires pour le groupe de trois et prévoit de les traiter après validation des fonctionnalités de base.

| Bonus | État |
| --- | --- |
| Chiffrement des communications | À valider |
| Chiffrement d’un dossier et export de la clé | À valider |
| Inventaire automatisé des services | À valider |
| Gestion de plusieurs clients | Trois connexions successives vérifiées sous Windows. Les connexions simultanées restent à valider. |

## Organisation et rendu

Chaque membre pousse ses changements sur sa branche. Le groupe relit les contributions dans des pull requests avant leur fusion dans `main`. Après validation de la version finale, un membre du groupe dépose le ZIP complet du dépôt sur la plateforme.
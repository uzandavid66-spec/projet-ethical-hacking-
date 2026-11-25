# Projet Ethical Hacking — Démonstration TCP

La démonstration de David utilise deux programmes Python qui communiquent en TCP sur `127.0.0.1:5000`. Le client envoie `Bonjour` et le serveur répond `OK`. Ayman a également réalisé un test avec son client de simulation sous Kali.

## Équipe

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman — membre 1 | Serveur TCP et client de simulation testés sous Kali | `ayman-membre-1` |
| Esra — membre 2 | Validation sous Windows proposée, à confirmer avec le groupe | À confirmer |
| David — membre 3 | Démonstration TCP sous Windows et Kali, diagnostic IPv4 local, lecture de données fictives, tests et documentation | `david-membre-3` |

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

Sous Kali, le fichier `test.png` contenait du texte de test. Ce résultat historique porte sur le transfert de données.

## Vérifications sous Kali

Les commandes ci-dessous ont été exécutées depuis la racine du dépôt sur Kali GNU/Linux 2026.2 avec Python 3.13.12. La branche de départ était `david-membre-3` au commit `1c4c84f` et l’arbre de travail était propre.

```sh
pwd
git status
git branch --show-current
git rev-parse --short HEAD
python3 --version
python3 -m unittest -v test_client test_tcp_integration
python3 -m unittest -v test_lin
python3 -m src.lin.diagnostic_ipv4
python3 -m src.lin.lecture_fictive
```

Pour l’essai TCP manuel, lancer le serveur dans un terminal et attendre son message d’écoute. Exécuter ensuite la deuxième commande dans un autre terminal. Le serveur s’arrête après la première connexion. Relancer alors la commande client pour vérifier le refus de connexion.

```sh
python3 src/c2/serveur_demo.py
python3 -m src.lin.client_local
python3 -m src.lin.client_local
```

L’essai a affiché `OK` avec le code de sortie `0`, puis `Connexion refusée` avec le code `1`. Le client accepte `--port` et utilise toujours `127.0.0.1`. Les tests TCP automatisés utilisent des ports libres attribués par le système.

Les trois tests existants et les dix nouveaux tests ont réussi. Les sockets TCP et Netlink ont été bloquées lors des premiers essais dans le bac à sable. Les vérifications réseau ont abouti après exécution hors bac à sable sur la même VM.

Le diagnostic IPv4 utilise la commande locale `ip` et affiche les adresses hors boucle locale à la demande. L’exemple de lecture affiche le contenu de `bonjour.txt` et les chemins relatifs des fichiers sous `src/lin/donnees_fictives/`, y compris dans les sous-dossiers. Il ignore les liens symboliques.

### Exigences Linux du professeur

L’énoncé du professeur est absent du dépôt. Le tableau recense les points Linux documentés et leur état de vérification. La correspondance avec les exigences officielles reste à confirmer.

| Point Linux | État | Résultat |
| --- | --- | --- |
| Échange TCP `Bonjour` → `OK` sur la boucle locale | Vérifié sur Kali | Essai en ligne de commande et tests d’intégration sur ports libres réussis |
| Client lancé sans serveur à l’écoute | Vérifié sur Kali | Refus explicite et code de sortie `1` |
| Diagnostic IPv4 hors boucle locale | Vérifié sur Kali | Deux interfaces affichées par la commande locale |
| Lecture et parcours de données fictives | Vérifié sur Kali | Lecture de `bonjour.txt` et affichage d’un fichier dans un sous-dossier |
| Filtrage des adresses de boucle locale et erreurs injectées | Simulation dans les tests | Sortie de `ip` et erreurs de socket ou de commande simulées |
| Aller-retour et transfert de données de test d’Ayman | Simulation historique | Résultats conservés dans le tableau des démonstrations |
| Capture d’écran réelle et échanges hors boucle locale | Hors périmètre | Aucune validation dans cette contribution |

## Arborescence de la branche de David

```text
.
├── README.md
├── test_client.py
├── test_lin.py
├── test_tcp_integration.py
├── bin/
└── src/
    ├── c2/
    │   ├── client_demo.py
    │   └── serveur_demo.py
    ├── lin/
    │   ├── client_local.py
    │   ├── diagnostic_ipv4.py
    │   ├── lecture_fictive.py
    │   └── donnees_fictives/
    │       ├── bonjour.txt
    │       └── exemples/
    │           └── note.txt
    └── win/
```

## Bonus du groupe de trois

Les notes du groupe prévoient de traiter ces bonus après les fonctionnalités de base. Leur caractère obligatoire reste à confirmer à partir de l’énoncé.

| Bonus | État |
| --- | --- |
| Chiffrement des communications | À valider |
| Chiffrement d’un dossier et export de la clé | À valider |
| Inventaire automatisé des services | À valider |
| Gestion de plusieurs clients | Trois connexions successives vérifiées sous Windows. Les connexions simultanées restent à valider. |

## Organisation et rendu

Chaque membre pousse ses changements sur sa branche. Le groupe relit les contributions dans des pull requests avant leur fusion dans `main`. Après validation de la version finale, un membre du groupe dépose le ZIP complet du dépôt sur la plateforme.

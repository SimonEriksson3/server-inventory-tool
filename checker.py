# Checker ska pinga servrar och uppdatera servarnas status
import subprocess
import sys

import storage

def ping_server(server):
    server_name = server["namn"]
    print(f"Kontrollerar {server_name}...")

    system = sys.platform
    arg = "-n" if system == "win32" else "-c" #Olika argument beroende på operativsystemet.
    status = ""

    try:
        result = subprocess.run(
            ["ping", arg, "2", server["adress"]],
            capture_output=True,
            timeout=5,
            text=True)
        if result.returncode == 0:
            print(f"{server_name} gick att nå.\n")
            status = "up"
        else:
            print(f"{server_name} kan inte nås.\n")
            status = "down"
    except FileNotFoundError:
        print("Fel: Ping kunde inte hittas i systemet. Ping måste vara tillgängligt för att kunna utföra kontroller av en server.")
        status = "unknown"
    except subprocess.TimeoutExpired:
        print(f"Fel: Kontrollen av {server_name} tog för lång tid och har avbrutits.")

    storage.update_status(server, status)

    return status
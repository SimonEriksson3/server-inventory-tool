# Checker ska pinga servrar och uppdatera servarnas status
import subprocess

import storage


def ping_server(server):
    server_name = server["namn"]
    print(f"Kontrollerar {server_name}...")

    result = subprocess.run(
        ["ping", server["adress"]],
        capture_output=True,
        text=True)

    status = ""

    if result.returncode == 0:
        print(f"{server_name} gick att nå.")
        status = "up"
    else:
        print(f"{server_name} kan inte nås.")
        status = "down"
    storage.update_status(server, status)
# Storage hanterar lagring och hämtning av JSON-data samt CSV-data
import csv
from datetime import datetime
import json
from pathlib import Path

import config


def load_servers(file_path):
    global servers # För att vi ska kunna nå den globala variabeln servers
    try:
        if Path(file_path).exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print("Fel: Kunde inte ladda servrar. Filen hittades inte.")
    except PermissionError as e:
        print(f"Fel: Kunde inte läsa filen {file_path}. {e}")
    except json.JSONDecodeError:
        print(f"Fel: Kunde inte läsa filen {file_path}. JSON-filen kan vara trasig")

servers = load_servers(config.get_servers_filepath())

def get_servers():
    return servers

def server_exists(name):
    for server in servers:
        if server["namn"].lower() == name.lower():
            return True
    return False

def add_server(name, address, environment, role):
    server_data = {
        "namn": name,
        "adress": address,
        "miljo": environment,
        "roll": role,
        "status": "unknown",
        "senast_kontrollerad": ""
    }
    servers.append(server_data)

def remove_server(server):
    servers.remove(server)

def export_report():
    directory = Path("rapporter")
    directory.mkdir(exist_ok=True)
    time = datetime.now()
    file_path = directory / f"{time.strftime('report_%Y-%m-%d_%H-%M')}.csv"
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"]
            )
            writer.writeheader()
            writer.writerows(servers)
        return file_path
    except PermissionError:
        print(f"PermissionError: Kunde inte skriva till filen {file_path}. ")
    except OSError as e:
        print(f"Fel: {e}")
    return None
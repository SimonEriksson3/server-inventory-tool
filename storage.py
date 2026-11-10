# Storage hanterar lagring och hämtning av JSON-data samt CSV-data
import csv
from datetime import datetime
import json

import config

def load_servers():
    file_path = config.get_servers_filepath()
    global servers # För att vi ska kunna nå den globala variabeln servers
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print("Fel: Kunde inte ladda servrar. Filen hittades inte.")
            return [] # Returnera ny tom lista
    except PermissionError as e:
        print(f"Fel: Kunde inte läsa filen {file_path}. {e}")
    except json.JSONDecodeError:
        print(f"Fel: Kunde inte läsa filen {file_path}. JSON-filen kan vara trasig")

def save_servers():
    file_path = config.get_servers_filepath()
    try:
        if file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    servers,
                    file,
                    indent=2,
                    ensure_ascii=False
                )
        else:
            print("Fel: Kunde inte skriva lagra nya servervärden. Filen hittades inte.")
    except PermissionError as e:
        print(f"Fel: Kunde inte läsa filen {file_path}. {e}")

servers = load_servers()

def get_servers():
    return servers

def update_status(server, status):
    time = datetime.now()
    server["status"] = status
    server["senast_kontrollerad"] = time.strftime("%Y-%m-%d %H:%M")


def server_exists(name):
    if servers:
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
    # Skapa mappen för rapporter om den inte finns.
    # Namnet på mappen anges i config.json
    directory = config.get_reports_filepath()
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
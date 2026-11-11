# Storage hanterar lagring och hämtning av JSON-data samt CSV-data
import csv
from datetime import datetime
import json

import config

def load_servers():
    file_path = config.get_servers_filepath()
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print("Fel: Kunde inte ladda servrar. Filen hittades inte.")
            return [] # Returnera ny tom lista
    except PermissionError as e:
        print(f"Fel: Kunde inte läsa filen {file_path}. Rättigheter saknas.")
    except json.JSONDecodeError:
        print(f"Fel: Kunde inte läsa filen {file_path}. JSON-filen kan vara trasig")
    except OSError as e:
        print(f"Fel: Ett fel uppstod under läsprocessen för {file_path}. {e}")

def save_servers():
    file_path = config.get_servers_filepath()
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                servers,
                file,
                indent=2,
                ensure_ascii=False
            )
    except PermissionError as e:
        print(f"Fel: Kunde inte skriva till filen {file_path}. Rättigheter saknas.")
    except OSError as e:
        print(f"Fel: Ett fel uppstod under skrivprocessen för {file_path}. {e}")

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
    save_servers()

def remove_server(server):
    servers.remove(server)
    save_servers()

def export_report(environment_filter = None):
    # Skapa mappen för rapporter om den inte finns.
    # Namnet på mappen anges i config.json
    directory = config.get_reports_filepath()
    directory.mkdir(exist_ok=True)
    time = datetime.now()
    file_path = directory / f"{time.strftime('report_%Y-%m-%d_%H-%M')}.csv"

    target_servers = []

    # Använd filtret om det finns.
    # Vi lägger till alla servrar
    if environment_filter:
        for server in servers:
            if server["miljo"] == environment_filter:
                target_servers.append(server)
    else:
        target_servers = servers.copy()

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"]
            )
            writer.writeheader()
            writer.writerows(target_servers)
        return file_path
    except PermissionError:
        print(f"Fel: Kunde inte skriva till filen {file_path}. Rättigheter saknas.")
    except OSError as e:
        print(f"Fel: Ett fel uppstod under skrivprocessen för {file_path}. {e}")
    return None
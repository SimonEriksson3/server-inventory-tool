# Storage hanterar lagring och hämtning av JSON-data samt CSV-data
import json
from pathlib import Path

servers = [

]

def load_servers(file_path):
    global servers # För att vi ska kunna nå den globala variabeln servers
    if Path(file_path).exists():
        with open(file_path, "r", encoding="utf-8") as file:
            servers = json.load(file)
    else:
        print("Fel: Kunde inte ladda servrar. Filen hittades inte.")

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
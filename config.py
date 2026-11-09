import json
from pathlib import Path

default_config = {"servers_sökväg": "servers.json",
                  "rapporter_sökväg": "rapporter"}

# Försöker läsa config.json och returnera den som en dictionary
def get_config():
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Fallback konfiguration
        print("Fel: Inga konfigurationer kunde laddas, filen hittades inte. Använder standardkonfigurationen.")
        return default_config

def get_servers_filepath():
    return Path(configuration["servers_sökväg"])

def get_reports_filepath():
    return Path(configuration["rapporter_sökväg"])

# Load configurations
configuration = get_config()
import json
import os
from pathlib import Path

default_config = {"servers_sökväg": "servrar.json",
                  "rapporter_sökväg": "rapporter"}
CONFIG_PATH = os.environ.get("INVENTORY_DATAFIL", "config.json")
IS_CLI = False

#I denna ordningen:
#Miljövariabel
#Config-fil
#Standardvärde

# Försöker läsa config.json och returnera den som en dictionary
def get_config():
    config_path = Path(CONFIG_PATH)
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
import json
import os
from pathlib import Path

default_config = {"servers_sökväg": "servrar.json",
                  "rapporter_sökväg": "rapporter"}

# Konfigurationen prioriterar denna ordningen:
# Miljövariabel (endast för filsökvägen till serverlistan, servrar.json)
# Config-fil
# Standardvärde

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
    return Path(configuration.get("servers_sökväg", "servrar.json"))

def get_reports_filepath():
    return Path(configuration.get("rapporter_sökväg", "rapporter"))

# Load configurations
configuration = get_config() #Laddar config.json
# Default sökväg till serverlistan ifall servers_sökväg inget hittas i config.json
default_path = configuration.get("servers_sökväg", "servrar.json")
# Till sist: använd miljövariabel om sådan finns.
configuration["servers_sökväg"] = os.environ.get("INVENTORY_DATAFIL", default_path)
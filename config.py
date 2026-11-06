import json
from pathlib import Path

# Försöker läsa config.json och returnera den som en dictionary
def get_config():
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        print("Fel: Inga konfigurationer kunde laddas. Filen hittas inte.")
        return None
# Main - startpunkt. Ska läsa argument med argparse

import menu
import config
import storage

# Load configurations
config = config.get_config()
# Fallback
if not config:
    config = {"servers_filepath": "servers.json"}
# Load servers from JSON
storage.load_servers(config["servers_filepath"])

menu.run()
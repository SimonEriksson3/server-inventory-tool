# Main - startpunkt. Ska läsa argument med argparse
import argparse
import sys

import config
import menu

parser = argparse.ArgumentParser(
    description="Server Inventory Tool")

parser.add_argument("--lista",
                    help="Lista alla servrar")
parser.add_argument("--miljo",
                    choices=["dev", "test", "prod"],
                    help="Filtrera baserat på miljö (dev, test, prod)")
parser.add_argument("--kontrollera",
                    help="Kontrollera en viss server")
parser.add_argument("--kontrollera-alla",
                    help="Kontrollera alla servrar")
parser.add_argument("--export",
                    help="Exporterar en rapport i CSV-format")

#sys.exit(0) = lyckad körning

if __name__ == "__main__":
    args = parser.parse_args()

    # Kontrollerar om programmet startar med argument eller inte.
    # Argument == CLI-mode.
    # Inga argument == GUI-mode.
    if len(sys.argv) != 1:
        config.IS_CLI = True
    else:
        menu.run()
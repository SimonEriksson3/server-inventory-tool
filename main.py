# Main - startpunkt. Ska läsa argument med argparse
import sys
import cli
import menu

if __name__ == "__main__":
    # Kontrollerar om programmet startar med argument eller inte.
    # Argument == CLI-mode.
    # Inga argument == GUI-mode.
    if len(sys.argv) != 1:
        cli.run()
    else:
        menu.run()
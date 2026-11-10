import argparse
import sys

import checker
import menu
import storage

parser = argparse.ArgumentParser(
    description="Server Inventory Tool")

parser.add_argument("--lista",
                    action="store_true",
                    help="Lista alla servrar")
parser.add_argument("--miljo",
                    choices=["dev", "test", "prod"],
                    help="Filtrera baserat på miljö (dev, test, prod)")
parser.add_argument("--server",
                    help="Visa en specifik server")
parser.add_argument("--kontrollera",
                    help="Kontrollera en viss server")
parser.add_argument("--kontrollera-alla",
                    action="store_true",
                    help="Kontrollera alla servrar")
parser.add_argument("--export",
                    action="store_true",
                    help="Exporterar en rapport i CSV-format")

servers = storage.get_servers()
environment_filter = None

# Exit codes:
# 0: allt gick bra
# 1: minst en server är nere
# 2: kunde inte skriva eller läsa fil

def run():
    args = parser.parse_args()

    global environment_filter

    # --server (lista specifik server)
    if args.server:
        server = find_by_name(args.server)
        menu.print_server_format(server)

    # --miljo (filtrera efter miljö när vi listar, kontrollerar eller exporterar)
    if args.miljo:
        environment_filter = args.miljo

    # --kontrollera (kontrollerar specifik server)
    if args.kontrollera:
        server = find_by_name(args.kontrollera)
        checker.ping_server(server)
        storage.save_servers()

    # --kontrollera-alla (kontrollerar alla servrar)
    if args.kontrollera_alla:
        check_all_servers()

    # --lista (listar alla servrar)
    if args.lista:
        list_servers()

    # --export (exporterar servrar)
    if args.export:
        export_report()

    # Om allt gick bra, avsluta med exit code 0
    sys.exit(0)

def list_by_environment(environment):
    for server in servers:
        if server["miljo"] == environment:
            menu.print_server_format(server)

def list_servers():
    if not environment_filter:
        menu.list_all_servers()
    else:
        list_by_environment(environment_filter)

def check_all_servers():
    server_down = False
    for server in servers:
        if environment_filter and server["miljo"] != environment_filter:
            continue
        if checker.ping_server(server) == "down":
            server_down = True
    storage.save_servers()
    #Om en server är nere, avsluta med exitcode 1
    if server_down:
        sys.exit(1)

def export_report():
    file_name = storage.export_report(environment_filter)
    if file_name is None:
        print("Fel: Kunde inte skriva till fil.")
        sys.exit(2)
    else:
        print(f"Rapport exporterad till {file_name}.")

def find_by_name(name):
    for server in servers:
        if server["namn"] == name:
            return server
    print(f"Fel: {name} hittades inte.")
    sys.exit(1)
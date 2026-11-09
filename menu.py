# Text-baserad meny.
import checker
import storage


# Starts the menu loop
def run():
    while True:
        # Uppdatera listan för varje iteration.
        # I praktiken vill man kanske att listan ska uppdateras inför varje operation för att få
        # färsk data.
        servers = storage.get_servers()
        print_menu()
        choice = get_user_choice(1, 8, "Gör ett val: ")

        if not storage.servers:
            if choice != 3 and choice != 8:
                print("Just nu finns inga servrar! Börja med att lägga till en server.")
                continue

        match(choice):
            case 1:
                list_all_servers(servers)
            case 2:
                list_by_environment(servers)
            case 3:
                add_server()
            case 4:
                remove_server(servers)
            case 5:
                check_server(servers)
            case 6:
                pass
            case 7:
                export_report(servers)
            case 8:
                break

def print_menu():
    print("=== Server Inventory Tool v0.1 ===\n")
    print("1. Lista alla servrar")
    print("2. Visa servrar i specifik miljö")
    print("3. Lägg till server")
    print("4. Ta bort server")
    print("5. Kontrollera server")
    print("6. Kontrollera alla servrar")
    print("7. Exportera rapport")
    print("8. Avsluta")

def list_all_servers(servers):
    print("--- Alla registrerade servrar ---")
    for server in servers:
        print_server_format(server)

def list_by_environment(servers):
    environment = get_user_input("Ange miljö: ")
    for server in servers:
        if server["miljo"] == environment:
            print_server_format(server)

def add_server():
    print("--- Lägg till server ---")
    name = get_user_input("Ange namn: ")
    address = get_user_input("Ange adress: ")

    environments = ["prod", "test", "dev"]
    environment = get_user_input("Ange miljö (dev/test/prod): ")
    while environment.lower() not in environments:
        print("Fel: Giltiga värden är dev, test eller prod. Försök igen.")
        environment = get_user_input("Ange miljö (dev/test/prod): ")

    role = get_user_input("Ange roll: ")

    if storage.server_exists(name):
        print(f"Fel: En server med namn {name} finns redan. ")
        return

    storage.add_server(name, address, environment, role)

def remove_server(servers):
    target_servers = select_servers(servers, "Ange vilka servrar du vill ta bort (separera med kommatecken): ")

    for server in target_servers:
        print(f"{server["namn"]} : {server["adress"]}")
    if get_confirmation("Är du säker på att du vill ta bort dessa servrar (ja/nej)?"):
        for target in target_servers:
            # Extra kontroll för radering av servrar i produktionsmiljön
            if target["miljo"] == "prod":
                if get_confirmation(f"{target["namn"]} är i produktion! \nÄr du säker på att du vill ta bort den (ja/nej)?"):
                    storage.remove_server(target)
            else:
                storage.remove_server(target)

def check_server(servers):
    target_servers = select_servers(servers, "Ange vilka servrar du vill kontrollera: ")

    for target in target_servers:
        checker.ping_servers(target)

def export_report(servers):
    file_name = storage.export_report(servers)
    if file_name is None:
        print("Kunde inte skriva till fil.")
    else:
        print(f"Rapport exporterad till {file_name}")

def print_server_format(server):
    print(f"{"Namn:":<25} {server["namn"]}")
    print(f"{"Adress:":<25} {server["adress"]}")
    print(f"{"Miljö:":<25} {server["miljo"]}")
    print(f"{"Roll:":<25} {server["roll"]}")
    print(f"{"Status:":<25} {server["status"]}")
    print(f"{"Senast kontrollerad:":<25} {server["senast_kontrollerad"]} \n")

def select_servers(servers, prompt):
    print("Vill du utföra åtgärden på samtliga servrar eller välja ut en/flera specifika servrar?\n")
    print("1. Alla servrar")
    print("2. Välj specifik(a) server/servrar\n")

    choice = get_user_choice(1, 2, "Gör ett val: ")

    target_servers = []

    match (choice):
        case 1:
            target_servers = servers.copy()
        case 2:
            # Om listan innehåller element
            for i in range(len(servers)):
                server = servers[i]
                print(f"{i + 1}:")
                print_server_format(server)

            servers_size = len(servers)
            choices = get_multiple_choices(1, servers_size, prompt)
            for number in choices:
                target_servers.append(servers[number - 1])
    return target_servers

# Input validering, tvingar fram korrekt inmatning i en loop
def get_user_choice(min, max, prompt):
    while True:
        user_input = input(prompt).strip()
        choice = 0

        try:
            choice = int(user_input)
            if choice >= min and choice <= max:
                return choice
            else:
                print(f"Fel: {user_input} är ett ogiltigt val. Välj ett av menyvalen ({min}-{max}).")
        except ValueError:
            print(f"Fel: Kunde inte tolka '{user_input}' som siffra. Ange en siffra mellan {min} och {max}.")
            continue

# Input validering för strängar
def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print("Fel: Ange giltigt värde")
            continue
        else:
            return user_input

#Ber användaren om ett eller flera val (siffror)
def get_multiple_choices(min, max, prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print("Fel: Ange antingen en enskild siffra eller flera siffror separerade med kommatecken (t.ex '1', eller '1, 2, 3, 4')")
            continue

        # Dela upp strängen i delar
        parts = user_input.split(',')
        numbers = [] # Listan med siffror vi ska returnera
        for part in parts:
            part = part.strip()
            try:
                server_number = int(part)
                if server_number < min or server_number > max:
                    print(f"Fel: {server_number} är inte ett giltigt värde och har hoppats över.")
                else:
                    if server_number not in numbers:
                        numbers.append(server_number)
            except ValueError:
                print(f"Fel: {part} ej tillåtet. Endast siffror tillåtna.")
                break
        else:
            if not numbers:
                continue
            return numbers

# Input validering för ja/nej-frågor
def get_confirmation(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input.lower() == "ja" or user_input.lower() == "j":
            return True
        elif user_input.lower() == "nej" or user_input.lower() == "n":
            return False
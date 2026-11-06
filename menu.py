# Text-baserad meny.
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

        match(choice):
            case 1:
                list_all_servers(servers)
            case 2:
                list_by_environment(servers)
            case 3:
                add_server()
            case 4:
                remove_server()
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
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
        print(f"Namn:                   {server["namn"]}")
        print(f"Adress:                 {server["adress"]}")
        print(f"Miljö:                  {server["miljo"]}")
        print(f"Roll:                   {server["roll"]}")
        print(f"Status:                 {server["status"]}")
        print(f"Senast kontrollerad:    {server["senast_kontrollerad"]} \n")

def list_by_environment(servers):
    environment = get_user_input("Ange miljö: ")
    for server in servers:
        if server["miljo"] == environment:
            print(f"Namn:                   {server["namn"]}")
            print(f"Adress:                 {server["adress"]}")
            print(f"Miljö:                  {server["miljo"]}")
            print(f"Roll:                   {server["roll"]}")
            print(f"Status:                 {server["status"]}")
            print(f"Senast kontrollerad:    {server["senast_kontrollerad"]} \n")

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

def remove_server():
    if storage.servers:  # Om listan innehåller element
        for i in range(len(storage.servers)):
            server = storage.servers[i]
            print(f"{i + 1}:")
            print(f"Namn:                   {server["namn"]}")
            print(f"Adress:                 {server["adress"]}")
            print(f"Miljö:                  {server["miljo"]}")
            print(f"Roll:                   {server["roll"]}")
            print(f"Status:                 {server["status"]}")
            print(f"Senast kontrollerad:    {server["senast_kontrollerad"]} \n")
        servers_size = len(storage.servers)
        choice = get_user_choice(1, servers_size, "Ange nummer för den server du vill ta bort: ")
        server_target = storage.servers[choice - 1]
        # Kontroll för radering av servrar i produktion
        if server_target["miljo"] == "prod":
            if get_confirmation("Denna server är i produktion! \nÄr du säker på att du vill ta bort den (ja/nej)?"):
                storage.remove_server(server_target)

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
                print(f"Fel: Ogiltigt val. Välj ett av menyvalen ({min}-{max}).")
        except ValueError:
            print(f"Fel: Ange en siffra mellan {min} och {max}.")
            return None

# Input validering för strängar
def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print("Fel: Ange giltigt värde")
            continue
        else:
            return user_input

# Input validering för ja/nej-frågor
def get_confirmation(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input.lower() == "ja" or user_input.lower() == "j":
            return True
        elif user_input.lower() == "nej" or user_input.lower() == "n":
            return False
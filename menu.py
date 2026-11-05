# Text-baserad meny.

# Starts the menu loop
def run():
    while True:
        print_menu()
        choice = get_user_input(1, 8, "Gör ett val: ")

        match(choice):
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
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

def get_user_input(min, max, prompt):
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

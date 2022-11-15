from const import ALLOWED_COMMANDS
from function import separator
from manager import manager

saldo = 1200.0
store = {}

file = open("store.txt", "w")
file.close()
operation_history = ()

while True:
    separator()
    print(f"Dozwolne komendy: {ALLOWED_COMMANDS}")
    command = input("Wpisz komendę: ")
    command = command.lower()

    if command not in ALLOWED_COMMANDS:
        print("Niepoprawna komenda!")
        continue

    if command == "exit":
        break

    elif command == "konto":
        manager.execute("konto", saldo=saldo)

    elif command == "magazyn":
        manager.execute("magazyn", store=store)

    elif command == "zakup":
        manager.execute("zakup", store=store, saldo=saldo)

    elif command == "saldo":
        manager.execute("saldo", saldo=saldo)

    elif command == "sprzedaz":
        manager.execute("sprzedaz", store=store, saldo=saldo)

    elif command == "przeglad":
        manager.execute("przeglad")


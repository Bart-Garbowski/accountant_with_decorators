class Manager:
    actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb

        return decorate

    def execute(self, name, *args, **kwargs):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self, *args, **kwargs)


manager = Manager()


@manager.assign("konto")
def konto(manager, saldo):
    print(f"Stan konta: {saldo} PLN")
    msg = f"Sprawdzono stan konta. Stan konta: {saldo}"
    with open("store.txt", "a") as file:
        file.write(f"Sprawdzenie stanu konta: {saldo} \n")


@manager.assign("magazyn")
def magazyn(manager, store):
    product_name = input("Nazwa towaru: ")

    product_info = store.get(product_name)
    if product_info:
        print(f"Informacje o produkcie: {product_name}")
        print(product_info)
    else:
        print(f"Nie ma towaru '{product_name}' w magazynie!")
    msg = f"Sprawdzono stan magazynu dla produktu {product_name}."
    with open("store.txt", "a") as file:
        file.write(f"Sprawdzenie stanu magazynu: {product_name} \n")


@manager.assign("zakup")
def zakup(manager, store, saldo):
    product_name = input("Nazwa produktu: ")
    price = input("Cena za sztukę: ")
    try:
        price = float(price)
    except ValueError:
        print("Prosze podawac tylko liczby! ")
        return

    count = input("Ilość: ")
    if count.isnumeric():
        count = int(count)
    else:
        print("Prosze podawac tylko liczby! ")
        return
    product_total_price = price * count

    if product_total_price > saldo:
        print(
            f"Za mało środków na koncie ({saldo}) na zakup towarów za cenę {product_total_price}!")
        return
    else:
        saldo -= product_total_price
        if product_name in store.keys():
            store[product_name]["price"] = price
            store[product_name]["count"] += count
        else:
            store[product_name] = {"price": price, "count": count}
            msg = f"Zakupiono product {product_name}. Ilosc sztuk: {count}. Za kwote {price} PLN. "
            with open("store.txt", "a") as file:
                file.write(f"zakup: {product_name}, {price}, {count}\n")


@manager.assign("saldo")
def saldo(manager, saldo):
    price = input("Kwota zmiany salda: ")
    try:
        price = float(price)
    except ValueError:
        print("Prosze podawac tylko liczby! ")
        return
    price = float(price)
    koment = input("Komentarz: ")
    if (saldo + price) >= 0:
        saldo += price
    else:
        print("Brak wystarczających środków na koncie!")
        return
    msg = f"Operacja na saldzie, nowe saldo po operacji = {saldo}. Komentarz: {koment}. Ile: {price} PLN"
    with open("store.txt", "a") as file:
        file.write(
            f"Operacja na saldzie, nowe saldo po operacji = {saldo}. Komentarz: {koment}. Ile: {price} PLN\n")


@manager.assign("sprzedaz")
def sprzedaz(manager, saldo, store):
    product_name = input("Nazwa produktu: ")

    if product_name not in store:
        print(f"Nie ma takiego produktu w magazynie!")
    else:
        if product_name in store.keys():
            count = input("Ilość: ")
            try:
                count = float(count)
            except ValueError:
                print("Prosze podawac tylko liczby! ")
                return
            price = store[product_name]["price"]
            ilosc_w_magazynie = store[product_name]["count"]
            price = float(price)
            count = int(count)

            if count > ilosc_w_magazynie:
                print(f"Niewystarczajaca ilosc {product_name} w magazynie! ")
                return
            total_price = price * count

            saldo += total_price
            if product_name in store.keys():
                store[product_name]["count"] -= count
                msg = f"Sprzedano product {product_name}. Ilosc sztuk: {count}. Za kwote {total_price} PLN. "
                with open("store.txt", "a") as file:
                    file.write(
                        f"Sprzedano product {product_name}. Ilosc sztuk: {count}. Za kwote {total_price} PLN.\n")


@manager.assign("przeglad")
def przeglad(manager):
    start = input("Od: ")
    end = input("Do: ")
    with open("store.txt") as file:
        if start == '' and end == '':
            for line in file.readlines():
                print(line.replace("\n", ""))
        elif start != '' and end == '':
            for line in file.readlines()[int(start):]:
                print(line.replace("\n", ""))
        elif start == '' and end != '':
            for line in file.readlines()[:int(end)]:
                print(line.replace("\n", ""))
        else:
            for line in file.readlines()[int(start):int(end)]:
                print(line.replace("\n", ""))

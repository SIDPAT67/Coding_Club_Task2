from openpyxl import Workbook, load_workbook
from tabulate import tabulate

class Item:
    def __init__(self, name, category, price, profit):
        self.name = name
        self.category = category
        self.price = price
        self.profit = profit

    def __str__(self):
        return self.name

class ItemRepository:
    def __init__(self):
        self.list = []

    def populate_data(self):
        wb = load_workbook("List_of_Items.xlsx")
        header = True
        for row in wb["Sheet1"]:
            if header:
                header = False
                continue

            name = row[0].value
            self.list.append(Item(row[0].value, row[1].value, row[2].value, row[3].value))
            pass

    def print_list(self):
        pass

items = ItemRepository()
items.populate_data()
items.print_list()

taxes = {
    "Plactic Ware": 5.0,
    "Celaning Products": 10.0,
    "Sports Eqiupment": 18.0,
    "Fashion": 18.0,
    "Staionary": 5.0,
    "Electronics": 28.0,
    "Dairy": 2.0,
    "Snacks & Drinks": 10.0
    }
cart = []

class Menu:
    def process_input(self, manager, option):
        pass

    def get_options_list(self):
        return self.options

    def print_header(self):
        pass

class ItemsListMenu(Menu):
    def __init__(self, category, search_query=""):
        self.title = "Enter index to add to cart"
        self.options = list([x for x in items.list if ((x.category == category or category == "") and search_query.lower() in x.name.lower())])
        pass

    def process_input(self, manager, option):
        item = self.options[option-1]
        cart.append(item)
        print(f"Added {item.name} to the cart.")
        pass

class CategoryListMenu(Menu):
    title = "List of Categories"

    def __init__(self):
        self.options = list(set([x.category for x in items.list]))

    def process_input(self, manager, option):
        manager.change_menu(ItemsListMenu(self.options[option-1]))
        pass

class CartMenu(Menu):
    title = "Cart"
    options = ["Remove Item", "Proceed to Pay"]

    def print_header(self):
        cart1 = [["Sr. No.", "Item", "Price"]]
        total_price = 0
        for i, item in enumerate(cart):
            total_price += float(item.price)            
            cart1.append([i+1, item.name, item.price])
        
        cart1.append(["", "Total", total_price])
        print(tabulate(cart1))

    def print_bill(self):
        bill = [["Sr. No.", "Item", "Price", "Tax", "Grand Total"]]
        total_price = 0
        total_tax = 0
        for i, item in enumerate(cart):
            total_price += float(item.price)
            total_tax += float(item.price) * taxes[item.category]/100
            
            bill.append([i+1, item.name, item.price, item.price * taxes[item.category]/100])
        
        bill.append(["", "Total", total_price, total_tax, total_price+total_tax])
        print(tabulate(bill))
        
    def process_input(self, manager, option):
        if option == 1:
            global cart
            index = int(input("Enter index of item to remove: "))
            del cart[index-1]

        if option == 2:
            self.print_bill()
            cart = []
            print("Thanks for purchasing.")
            manager.change_menu(MainMenu())

class MainMenu(Menu):
    title = "Main Menu"
    options = ["List of Categories ", "Search", "View Cart"]

    def process_input(self, manager, option):
        if option == 1:
            manager.change_menu(CategoryListMenu())
        elif option == 2:
            manager.change_menu(ItemsListMenu("", input("Enter search query: ")))
        elif option == 3:
            manager.change_menu(CartMenu())
        pass

class Admin_Menu(Menu):
    title = "Admin Menu"
    options = ["Store Catalogue"]
    def process_input(self, manager, option):
        if option == 1:
            table = [["Name", "Price", "Profit"]]
            for item in items.list:
                table.append([item.name, item.price, item.profit])
            print(tabulate(table))
        

class LoginMenu(Menu):
    title = "Login Portal"
    options = ["Student", "Admin"]

    def process_input(self, manager, option):
        if option == 1:
            input("Enter Student id: ")
            user_name = input("Enter Name: ")
            print("Welcome User, you are logged in as " + user_name)
            manager.change_menu(MainMenu())

        if option == 2:
            print("Admin login")
            adm_id = input("Enter Id No.: ")
            password = input("Enter Password: ")
            if adm_id == "Sam@1234" and password == "1234":
                print("Welcome Admin, You are logged in as Sam.")
                manager.change_menu(Admin_Menu())



class MenuManager:
    current_menu = LoginMenu()
    history = []

    def change_menu(self, menu, add_to_history=True):
        if add_to_history:
            self.history.append(self.current_menu)

        self.current_menu = menu
        pass

    def process_input(self):
        while True:
            options = [[self.current_menu.title]]
            for option in self.current_menu.options:
                options.append([f"{len(options)}) {option}"])

            if len(self.history) == 0:
                options = options + [[f"{len(options)}) Exit"]]
            else:
                options = options + [[f"{len(options)}) Back"]]

            self.current_menu.print_header()
            print(tabulate(options))
            choice = int(input()) - 1
            if choice < len(self.current_menu.options):
                self.current_menu.process_input(self, choice+1)
            else:
                if len(self.history) == 0:
                    return

                self.current_menu = self.history.pop()

manager = MenuManager()
manager.process_input()

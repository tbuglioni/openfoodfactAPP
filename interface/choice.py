from database import getter
from logic import link_api_db
from database import createdb
from database import adder


class Choice:
    def __init__(self):
        self.importer = link_api_db.LinkApiDb()
        self.getter = getter.Getter()
        self.adder = adder.Adder()
        self.create_db = createdb.CreateDb()
        self.choice_category = None
        self.choice_product = None
        self.run_app = True
        self.new_product = True


    def choose_in_db_menu(self):
        menu = ["(re)create the database, and download products", "update product", "use previous database" ]
        id = 1
        for elt in menu:
            print(id, elt)
            id += 1
        choice = int(input("select the number of your choice"))
        if choice == 1:
            self.importer.initialise_db()
        elif choice == 2:
            self.importer.update_db()
        elif choice == 3:
            self.importer.use_previous_db()
        else:
            print("you have to choose a number")
            self.choose_in_menu()


    def choose_categorie(self):
        try:
            list_of_choice = self.getter.get_x_categories(5)
            choice = int(input("choose the category you want (1-5) :"))
            self.choice_category = list_of_choice[choice - 1]
        except ValueError:
            print("you have to select a number between 1-5")
            self.choose_categorie()
        except IndexError:
            print("you have to select a number in the list only")
            self.choose_categorie()

    def choose_product(self):
        try:
            list_of_choice = self.getter.get_x_products(5, self.choice_category)
            choice = int(input("choose the product you want (1-5) :"))
            self.choice_product = list_of_choice[choice - 1]
        except ValueError:
            print("you have to select a number between 1-5")
            self.choose_product()
        except IndexError:
            print("you have to select a number in the list only")
            self.choose_product()

    def better_choice(self):
        return self.getter.get_better_choice(self.choice_product)

    def save_better_choice(self):
        pass

    def found_new_product(self):
        self.choose_categorie()
        self.choose_product()
        self.adder.save_better_choice(self.better_choice())


brain = Choice()
brain.choose_in_db_menu()
brain.found_new_product()


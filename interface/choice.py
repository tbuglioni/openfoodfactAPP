from database.getter import Getter
from logic.link_api_db import LinkApiDb
from database.adder import Adder


class Choice:
    """
    Interaction class, with interface and choice to
    - manage DB
    - check saved products
    - find new products
    """

    def __init__(self):
        self._importer = LinkApiDb()
        self._getter = Getter()
        self._adder = Adder()
        self._choice_category = None
        self._choice_product = None
        self._product_recommanded = None
        self._run_app = True
        self._new_product = True

    @property
    def importer(self):
        return self._importer

    @importer.setter
    def importer(self, new_value):
        self._importer = new_value

    @property
    def getter(self):
        return self._getter

    @getter.setter
    def getter(self, new_value):
        self._getter = new_value

    @property
    def adder(self):
        return self._adder

    @adder.setter
    def adder(self, new_value):
        self._adder = new_value

    @property
    def choice_category(self):
        return self._choice_category

    @choice_category.setter
    def choice_category(self, new_value):
        self._choice_category = new_value

    @property
    def choice_product(self):
        return self._choice_product

    @choice_product.setter
    def choice_product(self, new_value):
        self._choice_product = new_value

    @property
    def product_recommanded(self):
        return self._product_recommanded

    @product_recommanded.setter
    def product_recommanded(self, new_value):
        self._product_recommanded = new_value

    @property
    def run_app(self):
        return self._run_app

    @run_app.setter
    def run_app(self, new_value):
        self._run_app = new_value

    @property
    def new_product(self):
        return self._new_product

    @new_product.setter
    def new_product(self, new_value):
        self._new_product = new_value

    def choose_in_db_menu(self):
        """choice : manage database (create, update, use previous db) """
        print("------------------------------------------------")
        print("****************")
        print("*** DATABASE ***")
        print("****************")

        menu = [
            "(re)create the database, and download products",
            "update product",
            "use previous database",
        ]
        looper = 1
        for elt in menu:
            print(looper, elt)
            looper += 1
        choice = input("select the number of your choice : ")
        if choice == "1":
            self.importer.initialise_db()
        elif choice == "2":
            self.importer.update_db()
        elif choice == "3":
            self.importer.use_previous_db()
        else:
            print("you have to choose a number")
            self.choose_in_db_menu()

    def __choose_categorie(self):
        """ (best product: step1) choice : choose between 5 category / quite"""
        try:
            if self.new_product:
                list_of_choice = self.getter.get_x_categories(5)
                choice = input("choose the product you want (1-5) "
                               "or press q (quite) : ")
                if choice in "12345" and int(choice) < 6:
                    self.choice_category = list_of_choice[int(choice) - 1]
                elif choice == "q":
                    self.new_product = False
                else:
                    print("you have to select a number in the list only")
                    self.__choose_categorie()
            else:
                pass
        except ValueError:
            self.__choose_categorie()

    def __choose_product(self):
        """(best product: step2) choice : choose between 5 products
        (or less if not 5 in db) / quite"""
        try:
            if self.new_product:
                list_of_choice = (self.getter
                                  .get_x_products(5, self.choice_category))
                choice = input("choose the product you want (1-5) "
                               "or press q (quite) : ")
                if choice in "12345" and int(choice) < 6:
                    self.choice_product = list_of_choice[int(choice) - 1]
                elif choice == "q":
                    self.new_product = False
                else:
                    print("you have to select a number in the list only")
                    self.__choose_product()
            else:
                pass
        except ValueError:
            self.__choose_product()

    def __keep_better_choice(self):
        """(best product: step3), print the "best" product if exist,
        and add i in instance attribut"""
        if self.new_product:
            self.product_recommanded = self.getter.get_better_choice(
                self.choice_product
            )
            if self.product_recommanded is None:
                print("Ooops we don't find better product "
                      "for your choice sorry :/")
        else:
            pass

    def __choose_save_better_choice(self):
        """ (best product: step4) choice: save or not the "best" product"""
        if self.product_recommanded is not None and self.new_product is True:
            choice = input("save the recommendation ? y/n : ")
            if choice == "y".lower():
                self.adder.save_better_choice(self.product_recommanded)
            else:
                pass
        else:
            pass

    def __get_saved_recommendation(self):
        """ get te list of saved ("better") products """
        print("------------------------------------------------")
        print("********************")
        print("** Products saved **")
        print("********************")
        self.getter.get_save_recommendation()
        input("press enter to go 'menu'")

    def __found_new_product(self):
        """ get a better product through all steps"""
        print("------------------------------------------------")
        print("****************")
        print("* New product *")
        print("****************")

        self.__choose_categorie()
        self.__choose_product()
        self.__keep_better_choice()
        self.__choose_save_better_choice()

        self.choice_category = None
        self.choice_product = None
        self.product_recommanded = None
        self.new_product = True
        input("press enter to return to the menu")

    def __main_menu(self):
        """choice : all section of the app (product / manage db) """
        print("------------------------------------------------")
        print("****************")
        print("***** MENU *****")
        print("****************")

        menu = ["found product", "get saved products", "manage database"]
        id_looper = 1

        for elt in menu:
            print(id_looper, elt)
            id_looper += 1

        choice = input("select the number of your "
                       "choice or press q (quite) : ")
        if choice == "1":
            self.__found_new_product()
        elif choice == "2":
            self.__get_saved_recommendation()
        elif choice == "3":
            self.choose_in_db_menu()
        elif choice == "q":
            self.run_app = False
        else:
            print("you have to choose a number")
            self.__main_menu()

    def loop_app(self):
        """main loop:
        - menu : after all completed act --> go to menu
        - end : only by choice"""
        self.__main_menu()
        if self.run_app:
            self.loop_app()

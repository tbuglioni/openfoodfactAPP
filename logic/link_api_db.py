import peewee

from api.cleaner import Cleaner
from api.import_api import ImportApi
from database.createtables import CreateTables
from database.adder import Adder
from database.getter import Getter
from database.createdb import CreateDb


class LinkApiDb:
    """ manager to : API and DATABASE
    make a link between them """
    def __init__(self):
        self._importer = ImportApi()
        self._cleaner = Cleaner()
        self._create_table = CreateTables()
        self._create_db = CreateDb()
        self._adder = Adder()
        self._getter = Getter()

    @property
    def importer(self):
        return self._importer

    @importer.setter
    def importer(self, new_value):
        self._importer = new_value

    @property
    def cleaner(self):
        return self._cleaner

    @cleaner.setter
    def cleaner(self, new_value):
        self._cleaner = new_value

    @property
    def create_table(self):
        return self._create_table

    @create_table.setter
    def create_table(self, new_value):
        self._create_table = new_value

    @property
    def create_db(self):
        return self._create_db

    @create_db.setter
    def create_db(self, new_value):
        self._create_db = new_value

    @property
    def adder(self):
        return self._adder

    @adder.setter
    def adder(self, new_value):
        self._adder = new_value

    @property
    def getter(self):
        return self._getter

    @getter.setter
    def getter(self, new_value):
        self._getter = new_value

    def __recreate_db(self):
        """ delete and create database """
        self.create_db.recreate_db()

    def __create_db(self):
        """ create database """
        self.create_db.create_db()

    def __create_tables(self):
        """ create tables and connect to db """
        self.create_table.build_all_tables()
        self.adder.run_db()

    def __add_in_table(self, page_min, nbr_of_page):
        """ download, clean and add in db, product from api"""

        for elt in range(nbr_of_page):
            # download
            self.importer.api_parameters(page_min)
            self.importer.api_connexion()

            imported_file_status = self.importer.get_status_code()
            imported_file = self.importer.import_products()

            # clean
            self.cleaner.get_imported_file(imported_file, imported_file_status)
            self.cleaner.spliter()
            cleaned_file = self.cleaner.get_cleaned_list()

            # add in db
            self.adder.get_cleaned_list(cleaned_file)
            self.adder.add_in_all_tables(page_min, nbr_of_page)
            self.cleaner.delete_cleaned_list()
            page_min += 1

    def initialise_db(self):
        """ create new db, new table, with new products """
        self.__recreate_db()
        self.__create_tables()
        self.__add_in_table(1, 3)

    def update_db(self):
        """ update product in db """
        self.__create_tables()
        self.__add_in_table(1, 3)

    def use_previous_db(self):
        """ use previous db and check if db is not empty"""
        self.__create_db()
        try:
            number = self.getter.get_count_all_product()
            if number < 1000 or number is None:
                self.initialise_db()
            else:
                pass
        except peewee.ProgrammingError:
            self.initialise_db()

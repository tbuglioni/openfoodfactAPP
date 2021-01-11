from api import cleaner
from api import import_api
from database import createtables
from database import adder
from database import getter
from database import createdb
import peewee



class LinkApiDb:
    def __init__(self):
        self.importer = import_api.ImportApi()
        self.cleaner = cleaner.Cleaner()
        self.create_table = createtables.CreateTables()
        self.create_db = createdb.CreateDb()
        self.adder = adder.Adder()
        self.getter = getter.Getter()

    def _recreate_db(self):
        self.create_db.recreate_db()


    def _create_db(self):
        self.create_db.create_db()


    def _create_tables(self):
        self.create_table.build_all_tables()
        self.adder.run_db()

    def _add_in_table(self, page):
        self.importer.api_parameters(page)
        self.importer.api_connexion()

        imported_file_status = self.importer.get_status_code()
        imported_file = self.importer.import_products()

        self.cleaner.get_imported_file(imported_file, imported_file_status)
        self.cleaner.spliter()
        cleaned_file = self.cleaner.get_cleaned_list()

        self.adder.get_cleaned_list(cleaned_file)
        self.adder.add_in_all_tables()
        self.cleaner.delete_cleaned_list()


    def initialise_db(self):
        self._recreate_db()
        self._create_tables()
        self._add_in_table(1)
        self._add_in_table(2)
        self._add_in_table(3)

    def update_db(self):
        self._create_tables()
        self._add_in_table(1)
        self._add_in_table(2)
        self._add_in_table(3)

    def use_previous_db(self):
        """ use previous db and check if db is not empty"""
        self._create_db()
        try:
            number = self.getter.get_count_all_product()
            if number < 10 or number == None:
                self.initialise_db()
            else:
                pass
        except peewee.ProgrammingError:
            self.initialise_db()



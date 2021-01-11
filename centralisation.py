from api import cleaner
from api import import_api
from database import createtables
from database import getter
from database import adder
from database import createdb


class Centralisation:
    def __init__(self):
        self.importer = import_api.ImportApi()
        self.cleaner = cleaner.Cleaner()
        self.create_table = createtables.CreateTables()
        self.getter = getter.Getter()
        self.adder = adder.Adder()
        self.create_db = createdb.CreateDb()

    def create_db(self):
        self.create_db.create_db

    def create_tables(self):
        self.create_table.build_all_tables()
        self.adder.run_db()

    def add_in_table(self, page):

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
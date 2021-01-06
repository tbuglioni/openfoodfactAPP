from api import cleaner
from api import import_api
from database import modificator
from database import createtables


class Centralisation:
    def __init__(self):
        self.importer = import_api.ImportApi()
        self.cleaner = cleaner.Cleaner()
        self.create_table = createtables.CreateTables()
        self.adder = modificator.Modificator()

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




    def tester(self):
        self.adder.get_x_categories(5)
        self.adder.get_x_products(5, 2)
        self.adder.get_better_choice(3)

brain = Centralisation()
brain.create_tables()
brain.add_in_table(1)
brain.add_in_table(2)
brain.add_in_table(3)
brain.tester()
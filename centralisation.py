from api import cleaner
from api import import_api
from database import adder
from database import createtables


#instance
my_importer = import_api.ImportApi()
my_cleaner = cleaner.Cleaner()
my_create_tables = createtables.CreateTables()
my_adder = adder.Adder()

#api
my_importer.api_parameters()
my_importer.api_connexion()



#cleaner
imported_file_status = my_importer.get_status_code()
imported_file = my_importer.import_products()

my_cleaner.get_imported_file(imported_file, imported_file_status)

my_cleaner.spliter()

cleaned_file = my_cleaner.get_cleaned_list()


#create db/tables
my_create_tables.build_all_tables()


my_adder.run_db()
my_adder.get_cleaned_list(cleaned_file)
my_adder.add_in_all_tables()

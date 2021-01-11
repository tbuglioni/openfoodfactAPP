import peewee
import dotenv
from database.createtables import mysql_db
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory
from tqdm import tqdm
dotenv.load_dotenv()

class Adder:
    def __init__(self):
        self.cleaned_list = None

    def run_db(self):
        mysql_db.connect()

    def get_cleaned_list(self, the_cleaned_list):
        self.cleaned_list = the_cleaned_list

    def add_in_all_tables(self):
        for elements in tqdm(self.cleaned_list):
            actual_name = elements["name"]
            actual_store = elements["store"]  # 1 ou plus
            actual_nutriscore = elements["nutriscore"]
            actual_categories = elements["categories"]
            actual_url = elements["url"]

            if len(actual_categories) < 3:
                continue

            try:
                specific_nutriscore = (
                    Nutriscore.select()
                    .where(Nutriscore.nutriscores == actual_nutriscore)
                    .get()
                )
                Product.create(
                    shop=actual_store,
                    name=actual_name,
                    url=actual_url,
                    product_nutriscore=specific_nutriscore.id,
                )
            except:
                pass
            try:
                id_product = Product.select().where(Product.name == actual_name).get()
                for loop in actual_categories:
                    category_name = str(loop)
                    try:
                        AllCategory.create(category=category_name)
                    except:
                        pass
                    try:
                        id_category = (
                            AllCategory.select()
                            .where(AllCategory.category == category_name)
                            .get()
                        )
                        DescriptionProductCategory.create(
                            id_product=id_product, id_category=id_category
                        )
                    except peewee.IntegrityError:
                        pass
            except:
                pass

    def save_better_choice(self, id_product):

        res = (Product
               .update(record=1)
               .where(Product.id == id_product)
               .execute())


        res



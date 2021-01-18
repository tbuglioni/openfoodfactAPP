import peewee
import dotenv

from database.createtables import mysql_db
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory
import tqdm

dotenv.load_dotenv()


class Adder:
    """ add in database all cleaned products from api"""

    def __init__(self):
        self._cleaned_list = None

    @property
    def cleaned_list(self):
        return self._cleaned_list

    @cleaned_list.setter
    def cleaned_list(self, new_value):
        self._cleaned_list = new_value

    @staticmethod
    def run_db():
        """ connection to the database """
        mysql_db.connect()

    def get_cleaned_list(self, the_cleaned_list):
        """ add in attribut the list of product cleaned """
        self.cleaned_list = the_cleaned_list

    def add_in_all_tables(self, page, loop):
        """ add each products in the database """
        for elements in tqdm.tqdm(
                self.cleaned_list, desc="page: {}/{}".format(page, loop)
        ):
            actual_name = elements["name"]
            actual_store = elements["store"]  # 1 ou plus
            actual_nutriscore = elements["nutriscore"]
            actual_categories = elements["categories"]
            actual_url = elements["url"]

            if (
                    len(actual_categories) < 3
            ):  # product with more than 2 category (for precision when we find product)
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
            except peewee.IntegrityError:
                pass

            try:
                id_product = Product.select().where(Product.name == actual_name).get()
                for loop in actual_categories:
                    category_name = str(loop)
                    try:
                        AllCategory.create(category=category_name)
                    except peewee.IntegrityError:
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
            except peewee.OperationalError:
                pass

    @staticmethod
    def save_better_choice(id_product):
        """ save as better choice, one product"""

        save_product = (
            Product.update(record=1).where(Product.id == id_product).execute()
        )
        save_product  # this variable make the save possible

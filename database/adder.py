import peewee
import dotenv
import os

dotenv.load_dotenv()

mysql_db = peewee.MySQLDatabase(
    "openfoodfact",
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    host="localhost", )


class Database(peewee.Model):
    class Meta:
        database = mysql_db  # This model uses the "openfoodfact.db" database.
        id = peewee.AutoField(primary_key=True, unique=True)


class nutriscore(Database):
    nutriscores = peewee.FixedCharField(1, unique=True, null=False)


class product(Database):
    name = peewee.CharField(unique=True, null=False)
    record = peewee.SmallIntegerField(1, default=0)
    shop = peewee.CharField(null=False)
    url = peewee.CharField(null=False)
    product_nutriscore = peewee.ForeignKeyField(nutriscore, backref='products')


class category(Database):
    category = peewee.CharField(unique=True, null=False)


class description_product_category(Database):
    id_product = peewee.ForeignKeyField(product, backref='description_product_category')
    id_category = peewee.ForeignKeyField(category, backref='description_product_category')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('id_product', 'id_category'), True),
        )

class Adder:

    def __init__(self):
        self.cleaned_list = None

    def run_db(self):
        mysql_db.connect()

    def close_db(self):
        mysql_db.close()

    def get_cleaned_list(self, the_cleaned_list):
        self.cleaned_list = the_cleaned_list

    def add_in_all_tables(self):
        for elements in self.cleaned_list:
            actual_name = elements['name']
            actual_store = elements['store'] # 1 ou plus
            actual_nutriscore = elements['nutriscore']
            actual_categories = elements['categories']
            actual_url = elements['url']
            try :
                specific_nutriscore = nutriscore.select().where(nutriscore.nutriscores == actual_nutriscore).get()
                product.create(shop=actual_store,
                               name=actual_name,
                               url=actual_url,
                               product_nutriscore=specific_nutriscore.id,
                               )
            except:
                pass
            id_product = product.select().where(product.name == actual_name).get()
            for loop in actual_categories:
                category_name = str(loop)
                try :
                    category.create(category=category_name)
                except:
                    pass
                try:
                    id_category = category.select().where(category.category == category_name).get()
                    description_product_category.create(id_product=id_product, id_category=id_category)
                except peewee.IntegrityError:
                    pass





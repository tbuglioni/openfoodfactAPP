import peewee
import dotenv
import os
dotenv.load_dotenv()

class CreateDb:
    def __init__(self):
        self.mysql_db = peewee.MySQLDatabase(
    "openfoodfact",
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    host="localhost",)

    def create_tables(self):
        class Database(peewee.Model):
            class Meta:
                database = self.mysql_db  # This model uses the "openfoodfact.db" database.
                id = peewee.AutoField(primary_key=True, unique=True)

        class nutriscore(Database):
            nutriscore = peewee.FixedCharField(1, unique=True, null=False)

        class product(Database):
            name = peewee.CharField(unique=True, null=False)
            record = peewee.SmallIntegerField(1, default=0)
            shop = peewee.CharField(null=False)
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
        self.mysql_db.connect()
        self.mysql_db.create_tables([product, nutriscore,description_product_category,category])
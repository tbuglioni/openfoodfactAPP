import peewee
import dotenv
import os
import database.createdb

dotenv.load_dotenv()
database.createdb.CreateDb().create_db()


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


class CreateTables:

    def build_all_tables(self):
        mysql_db.connect()
        mysql_db.create_tables([product, nutriscore, description_product_category, category])

        data = [
            {nutriscore.nutriscores: 'a'},
            {nutriscore.nutriscores: 'b'},
            {nutriscore.nutriscores: 'c'},
            {nutriscore.nutriscores: 'd'},
            {nutriscore.nutriscores: 'e'}
        ]
        with mysql_db.atomic():
            nutriscore.insert_many(data).execute()

        mysql_db.close()
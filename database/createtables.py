import peewee
import dotenv
import os



dotenv.load_dotenv()


mysql_db = peewee.MySQLDatabase(
    "openfoodfact",
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    host="localhost",
)


class Database(peewee.Model):
    class Meta:
        database = mysql_db  # This model uses the "openfoodfact.db" database.
        id = peewee.AutoField(primary_key=True, unique=True)


class Nutriscore(Database):
    nutriscores = peewee.FixedCharField(1, unique=True, null=False)


class Product(Database):
    name = peewee.CharField(unique=True, null=False)
    record = peewee.SmallIntegerField(1, default=0)
    shop = peewee.CharField(null=False)
    url = peewee.CharField(null=False)
    product_nutriscore = peewee.ForeignKeyField(Nutriscore, backref="products")


class AllCategory(Database):
    category = peewee.CharField(unique=True, null=False)


class DescriptionProductCategory(Database):
    id_product = peewee.ForeignKeyField(Product, backref="description_product_category")
    id_category = peewee.ForeignKeyField(
        AllCategory, backref="description_product_category"
    )

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (("id_product", "id_category"), True),
        )


class CreateTables:
    def build_all_tables(self):
        mysql_db.create_tables(
            [Product, Nutriscore, DescriptionProductCategory, AllCategory]
        )
        try:
            data = [
                {Nutriscore.nutriscores: "a"},
                {Nutriscore.nutriscores: "b"},
                {Nutriscore.nutriscores: "c"},
                {Nutriscore.nutriscores: "d"},
                {Nutriscore.nutriscores: "e"},
            ]
            with mysql_db.atomic():
                Nutriscore.insert_many(data).execute()
        except peewee.IntegrityError:
            pass
        mysql_db.close()

    def connect_to_db(self):
        mysql_db.connect()

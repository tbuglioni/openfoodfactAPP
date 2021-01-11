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


class SandBox:
    def get_x_categories(self, nbr_of_values):
        query = AllCategory.select().order_by(peewee.fn.Rand()).limit(nbr_of_values)
        print(" ---- liste des categories ---- ")
        for elt in query:
            print(elt.id, elt.category)

    def get_x_products(self, nbr_of_values, category_to_find):
        count_all_value = (
            DescriptionProductCategory.select()
            .where(DescriptionProductCategory.id_category == category_to_find)
            .count()
        )
        if count_all_value < nbr_of_values:
            nbr_of_values = count_all_value
        print(" ---- liste d'aliments avec cette categorie ----")
        print(
            "il y a en tout",
            count_all_value,
            "produit(s) avec cette categorie, en voici une partie",
        )
        query = (
            Product.select(Product, DescriptionProductCategory)
            .join(DescriptionProductCategory)
            .where(DescriptionProductCategory.id_category_id == category_to_find)
            .order_by(peewee.fn.Rand())
            .limit(nbr_of_values)
        )

        for loop in query:
            print(loop.id, loop.name)

    def get_better_choice(self, selected_product_id):
        print(
            " ---- analyse des categories du produit selectionné par ordre de presence dans la BD----"
        )

        # recuperer les caracteristiques du produit
        subquery = DescriptionProductCategory.select(
            DescriptionProductCategory.id_category
        ).where(DescriptionProductCategory.id_product == selected_product_id)

        # retourner les caracteristiques les plus importantes (3)
        query = (
            DescriptionProductCategory.select(
                DescriptionProductCategory.id_category,
                peewee.fn.COUNT(DescriptionProductCategory.id_category).alias("count"),
            )
            .where(DescriptionProductCategory.id_category.in_(subquery))
            .group_by(DescriptionProductCategory.id_category)
            .order_by(peewee.fn.COUNT(DescriptionProductCategory.id_category).desc())
            .limit(3)
        )
        final_choice = []
        for cate in query:
            product_number = cate.id_category
            final_choice.append(cate.id_category)
            print(product_number)
        print(final_choice)

        nutri_product = (
            Product.select(Product.product_nutriscore)
            .where(Product.id == selected_product_id)
            .get()
        )
        nutri_product = nutri_product.product_nutriscore
        nutri_product = str(nutri_product)
        nutri_product = [int(s) for s in nutri_product.split() if s.isdigit()]
        nutri_product = int(nutri_product[0])

        if nutri_product > 1:
            nutri_product -= 1

        # retouner le bon produit
        DPCB = DescriptionProductCategory.alias()
        DPCC = DescriptionProductCategory.alias()
        scnd_query = (
            DescriptionProductCategory.select(
                DescriptionProductCategory.id_product,
                DescriptionProductCategory.id_category,
                DPCB.id_category,
                DPCC.id_category,
                Product.product_nutriscore,
            )
            .join(DPCB, on=(DescriptionProductCategory.id_product == DPCB.id_product))
            .join(DPCC, on=(DescriptionProductCategory.id_product == DPCB.id_product))
            .join(Product, on=(Product.id == DescriptionProductCategory.id_product))
            .where(
                (DescriptionProductCategory.id_category == final_choice[0])
                & (DPCB.id_category == final_choice[1])
                & (DPCC.id_category == final_choice[2])
                & (Product.product_nutriscore == nutri_product)
                & (DescriptionProductCategory.id_product != selected_product_id)
            )
            .order_by(peewee.fn.Rand())
            .limit(1)
        )

        for cate in scnd_query:
            print(cate.id_product)

            query = (
                Product.select()
                .join(
                    DescriptionProductCategory,
                    on=(DescriptionProductCategory.id_product == Product.id),
                )
                .join(
                    AllCategory,
                    on=(DescriptionProductCategory.id_category == AllCategory.id),
                )
                .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
                .where(Product.id == cate.id_product)
                .limit(1)
            )
            for elt in query:
                print(elt.name, elt.shop, elt.url, elt.product_nutriscore.nutriscores)


mysandbox = SandBox()

mysandbox.get_better_choice(2)

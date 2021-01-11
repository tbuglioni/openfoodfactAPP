import peewee
import dotenv
from database.createtables import mysql_db
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory
from tqdm import tqdm

dotenv.load_dotenv()


class Modificator:
    def __init__(self):
        self.cleaned_list = None

    def run_db(self):
        mysql_db.connect()

    def close_db(self):
        mysql_db.close()

    def get_cleaned_list(self, the_cleaned_list):
        self.cleaned_list = the_cleaned_list

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

            # print("le produit selectionné à la caracteristique :", product_number)
            # a = str(category_number)
            # b = [int(s) for s in a.split() if s.isdigit()] # pour obtenir en int la categorie
            # print("voici le texte : ", b, b[0] + 1)

        # obtenir produit avec au mois 3 categories pareils et un nutriscore sup

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

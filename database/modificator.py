import peewee
import dotenv
from database.createtables import mysql_db
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory
from tqdm import tqdm

# to do :
# get importer 5 catégories (aleatoire) ok
# get importer 5 noms de produits (aleatoire) avec une catégorie (aleatoire) ok
# choice selectionner le nom d'un produit
# get obtenir un substitut  - en cours
# save enregistrer le substitut

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
        print("il y a en tout", count_all_value, "produit(s) avec cette categorie, en voici une partie")
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
        print(" ---- analyse du produit selectionné ----")
        # obtenir categories d'un produit ok
        # obtenir nutriscore d'un produit OK
        origin_product_categories = []
        origin_product_categories_dict = {}
        i = 0
        query = (
            DescriptionProductCategory
            .select(Product.product_nutriscore, DescriptionProductCategory.id_category)
            .join(Product, on=(Product.id == DescriptionProductCategory.id_product_id))
            .where(Product.id == selected_product_id)
        )

        for cate in query:
            origin_product_nutriscore = cate.id_product.product_nutriscore
            category_number = cate.id_category

            print("le produit selectionné à la caracteristique :", category_number)
            print(type(category_number))

            origin_product_categories.append(category_number)
            origin_product_categories_dict[i] = cate.id_category
            i += 1



        print("le nutriscore est (en chiffre) : ", origin_product_nutriscore)
        if origin_product_nutriscore == Nutriscore(1):
            print("le chiffre est excelent")


        print("les categories du produit sont :", origin_product_categories)
        print( origin_product_categories_dict)

        #obtenir produit avec au mois 3 categories pareils et un nutriscore sup




    def add_in_all_tables(self):
        for elements in tqdm(self.cleaned_list):
            actual_name = elements["name"]
            actual_store = elements["store"]  # 1 ou plus
            actual_nutriscore = elements["nutriscore"]
            actual_categories = elements["categories"]
            actual_url = elements["url"]

            if len(actual_categories)<3:
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



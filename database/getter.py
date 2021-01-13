import peewee
import dotenv
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory


dotenv.load_dotenv()


class Getter:
    def __init__(self):
        self.product_category_origine = []
        self.product_nutriscore_target = None

    def get_cleaned_list(self, the_cleaned_list):
        self.cleaned_list = the_cleaned_list

    def get_x_categories(self, nbr_of_values):
        query = AllCategory.select().order_by(peewee.fn.Rand()).limit(nbr_of_values)
        print(" ---- category of product ---- ")
        list_of_choice = []
        id = 1
        for elt in query:
            print(id, elt.category)
            list_of_choice.append(elt.id)
            id += 1
        return list_of_choice

    def get_x_products(self, nbr_of_values, category_to_find):
        count_all_value = (
            DescriptionProductCategory.select()
            .where(DescriptionProductCategory.id_category == category_to_find)
            .count()
        )
        if count_all_value < nbr_of_values:
            nbr_of_values = count_all_value

        print(" ---- products with this category ----")
        print(
            "there is :",
            count_all_value,
            "product in the db")
        query = (
            Product.select(Product, DescriptionProductCategory, Nutriscore)
            .join(DescriptionProductCategory, on=(Product.id == DescriptionProductCategory.id_product))
            .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
            .where(DescriptionProductCategory.id_category_id == category_to_find)
            .order_by(peewee.fn.Rand())
            .limit(nbr_of_values)
        )
        list_of_choice = []
        id = 1
        for loop in query:
            print(id, loop.name, "(nutriscore :", loop.product_nutriscore.nutriscores,")")
            id+=1
            list_of_choice.append(loop.id)
        return list_of_choice


    def get_caracteristiques_origine(self, selected_product_id):

        # get all category from origin product
        subquery = DescriptionProductCategory.select(
            DescriptionProductCategory.id_category
        ).where(DescriptionProductCategory.id_product == selected_product_id)

        # get 3 most presents category
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
        self.product_category_origine = []
        for cate in query:
            product_number = cate.id_category
            self.product_category_origine.append(cate.id_category)

    def get_int_from_peewee(self, enter):
        exit = enter
        exit = str(exit)
        exit = [int(s) for s in exit.split() if s.isdigit()]
        exit = int(exit[0])
        return exit

    def get_nutriscore_target(self, selected_product_id):
        nutri_product = (
            Product.select(Product.product_nutriscore)
                .where(Product.id == selected_product_id)
                .get()
        )
        self.product_nutriscore_target = self.get_int_from_peewee(nutri_product.product_nutriscore)

        if self.product_nutriscore_target > 1:
            self.product_nutriscore_target -= 1

    def find_the_better_choice(self, selected_product_id):
        # retouner le bon produit
        DPCB = DescriptionProductCategory.alias()
        DPCC = DescriptionProductCategory.alias()
        query = (
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
                (DescriptionProductCategory.id_category == self.product_category_origine[0])
                & (DPCB.id_category == self.product_category_origine[1])
                & (DPCC.id_category == self.product_category_origine[2])
                & (Product.product_nutriscore == self.product_nutriscore_target)
                & (DescriptionProductCategory.id_product != selected_product_id)
            )
                .order_by(peewee.fn.Rand())
                .limit(1)
        )

        for cate in query:
            query = (
                Product.select()
                    .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
                    .join(DescriptionProductCategory, on=(Product.id == DescriptionProductCategory.id_product))
                    .join(AllCategory, on=(DescriptionProductCategory.id_category == AllCategory.id))
                    .where(Product.id == cate.id_product)
                    .limit(1)
            )
            size = len(query)
            if size > 0:
                for elt in query:
                    print("===============================================")
                    print("------*** product name :", elt.name, "***------")
                    print(" nutriscore --> ", elt.product_nutriscore.nutriscores)
                    print(" shop --------> ", elt.shop)
                    print(" url  --------> ", elt.url)
                    print("===============================================")
                    print("===============================================")
                    return self.get_int_from_peewee(elt.id)
            else:
                print("Ooops we don't find better product for your choice sorry :/")

    def get_better_choice(self, selected_product_id):
        self.get_caracteristiques_origine(selected_product_id)
        self.get_nutriscore_target(selected_product_id)
        return self.find_the_better_choice(selected_product_id)

    def get_count_all_product(self):
        quantity = Product.select(peewee.fn.COUNT(Product.id).alias("count")).get()
        return int(quantity.count)

    def get_save_recommendation(self):
        print("list of products saved")
        query = (Product
                 .select()
                 .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
                 .where(Product.record == 1))
        id = 1
        for elt in query:

            print(id,
                  "product name:", elt.name,
                  "// nutriscore:", elt.product_nutriscore.nutriscores,
                  "// shop:", elt.shop,
                  "// url:", elt.url
                  )
            id += 1
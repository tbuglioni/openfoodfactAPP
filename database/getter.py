import peewee
import dotenv
from database.createtables import Nutriscore
from database.createtables import Product
from database.createtables import AllCategory
from database.createtables import DescriptionProductCategory


dotenv.load_dotenv()


class Getter:
    """ get elements from database """
    def __init__(self):
        self._product_category_origin = []
        self._product_nutriscore_target = None

    @property
    def product_category_origin(self):
        return self._product_category_origin

    @product_category_origin.setter
    def product_category_origin(self, new_value):
        self._product_category_origin = new_value

    @property
    def product_nutriscore_target(self):
        return self._product_nutriscore_target

    @product_nutriscore_target.setter
    def product_nutriscore_target(self, new_value):
        self._product_nutriscore_target = new_value

    @staticmethod
    def get_x_categories(nbr_of_values):
        """ get x category of product from db """
        query = AllCategory.select().order_by(peewee.fn.Rand()).limit(nbr_of_values)
        print(" ---- category of product ---- ")
        list_of_choice = []
        id_looper = 1
        for elt in query:
            print(id_looper, elt.category)
            list_of_choice.append(elt.id)
            id_looper += 1
        return list_of_choice

    @staticmethod
    def get_x_products(nbr_of_values, category_to_find):
        """ get x products with 1 specific category"""
        count_all_value = (
            DescriptionProductCategory.select()
            .where(DescriptionProductCategory.id_category == category_to_find)
            .count()  # check the number of product
        )
        if count_all_value < nbr_of_values:  # if not enough products
            nbr_of_values = count_all_value

        print(" ---- products with this category ----")
        print("there is :", count_all_value, "product in the db")
        query = (
            Product.select(Product, DescriptionProductCategory, Nutriscore)
            .join(
                DescriptionProductCategory,
                on=(Product.id == DescriptionProductCategory.id_product),
            )
            .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
            .where(DescriptionProductCategory.id_category_id == category_to_find)
            .order_by(peewee.fn.Rand())
            .limit(nbr_of_values)
        )
        list_of_choice = []
        id_loop = 1
        for loop in query:
            print(
                id_loop, loop.name, "(nutriscore :", loop.product_nutriscore.nutriscores, ")"
            )
            id_loop += 1
            list_of_choice.append(loop.id)
        return list_of_choice

    def get_category_origin(self, selected_product_id):
        """ get category from 1 product """

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
        self.product_category_origin = []
        for cate in query:
            self.product_category_origin.append(cate.id_category)

    @staticmethod
    def __get_int_from_peewee(enter):
        """ extract int from database element"""
        new_int = enter
        new_int = str(new_int)
        new_int = [int(s) for s in new_int.split() if s.isdigit()]
        new_int = int(new_int[0])
        return new_int

    def __get_nutriscore_target(self, selected_product_id):
        """ get the nutriscore of 1 product """
        nutri_product = (
            Product.select(Product.product_nutriscore)
            .where(Product.id == selected_product_id)
            .get()
        )
        self.product_nutriscore_target = self.__get_int_from_peewee(
            nutri_product.product_nutriscore
        )

        if self.product_nutriscore_target > 1:
            self.product_nutriscore_target -= 1

    def __find_the_better_choice(self, selected_product_id):
        """ find 1 product with higher nutriscore and 3 identical category """
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
                (
                    DescriptionProductCategory.id_category
                    == self.product_category_origin[0]
                )
                & (DPCB.id_category == self.product_category_origin[1])
                & (DPCC.id_category == self.product_category_origin[2])
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
                .join(
                    DescriptionProductCategory,
                    on=(Product.id == DescriptionProductCategory.id_product),
                )
                .join(
                    AllCategory,
                    on=(DescriptionProductCategory.id_category == AllCategory.id),
                )
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
                    return self.__get_int_from_peewee(elt.id)
            else:
                print("Ooops we don't find better product for your choice sorry :/")

    def get_better_choice(self, selected_product_id):
        """ get the better choice (all steps) """
        self.get_category_origin(selected_product_id)
        self.__get_nutriscore_target(selected_product_id)
        return self.__find_the_better_choice(selected_product_id)

    @staticmethod
    def get_count_all_product():
        """ get the number of product in the database """
        quantity = Product.select(peewee.fn.COUNT(Product.id).alias("count")).get()
        return int(quantity.count)

    @staticmethod
    def get_save_recommendation():
        """ get the product saved (best product) in the database"""
        print("list of products saved : ")
        query = (
            Product.select()
            .join(Nutriscore, on=(Product.product_nutriscore == Nutriscore.id))
            .where(Product.record == 1)
        )
        id_looper = 1
        for elt in query:

            print(
                id_looper,
                "product name:",
                elt.name,
                "// nutriscore:",
                elt.product_nutriscore.nutriscores,
                "// shop:",
                elt.shop,
                "// url:",
                elt.url,
            )
            id_looper += 1

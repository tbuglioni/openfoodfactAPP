class Cleaner:
    def __init__(self):
        """ clean all products imported from the api"""
        self._imported_file = None
        self._cleaned_list = []

    @property
    def imported_file(self):
        return self._imported_file

    @imported_file.setter
    def imported_file(self, new_value):
        self._imported_file = new_value

    @property
    def cleaned_list(self):
        return self._cleaned_list

    @cleaned_list.setter
    def cleaned_list(self, new_value):
        self._cleaned_list = new_value

    def get_imported_file(self, file_to_get, status_code):
        """ get previous import from api--> attribut and check status code"""
        if status_code == 200:
            self.imported_file = file_to_get

    @staticmethod
    def __cleaner_mono_entry(text_to_check):
        """ clean 1 element without split"""
        return str(text_to_check).lower().strip()

    @staticmethod
    def __cleaner_multiples_entry(product_to_clean):
        """ clean x elements with split (list)"""
        mini_str = str(product_to_clean).lower()
        mini_list = mini_str.split(",")
        cleaned_list = []
        for elt in mini_list:
            elt2 = elt.strip()

            cleaned_list.append(elt2)

        return cleaned_list

    def spliter(self):
        """ split and clean all products from api"""
        if self.imported_file is not None:
            for product in self.imported_file:
                try:
                    if (
                        len(product["product_name"]) > 2  # product.get("product_name")
                        and product["nutrition_grades"]
                        and product["stores"]
                        and product["categories"]
                        and product["url"]
                    ):
                        new_name = self.__cleaner_mono_entry(product["product_name"])
                        new_nutrition_grades = self.__cleaner_mono_entry(
                            product["nutrition_grades"]
                        )
                        new_stores = self.__cleaner_mono_entry(product["stores"])
                        new_categories = self.__cleaner_multiples_entry(
                            product["categories"]
                        )
                        new_url = product["url"]
                        self.cleaned_list.append(
                            {
                                "name": new_name,
                                "nutriscore": new_nutrition_grades,
                                "store": new_stores,
                                "categories": new_categories,
                                "url": new_url,
                            }
                        )

                except KeyError:  # when the product don't match with all category required
                    pass

    def get_cleaned_list(self):
        """ return the list after split & clean"""
        return self.cleaned_list

    def delete_cleaned_list(self):
        """ delete the attribut with le list cleaned"""
        self.cleaned_list = []

class Cleaner:

    def __init__(self):
        self.imported_file = None
        self.cleaned_list = []

    def get_imported_file(self, file_to_get, status_code):
        if status_code == 200:
            self.imported_file = file_to_get

    def cleaner_mono_entry(self, text_to_check):
        return str(text_to_check).lower().strip()

    def cleaner_multiples_entry(self, product_to_clean):
        mini_str = str(product_to_clean).lower()
        mini_list = mini_str.split(",")
        for elt in mini_list:
            elt2 = elt.strip()
            cleaned_list = []
            cleaned_list.append(elt2)

        return cleaned_list

    def spliter(self):
        if self.imported_file is not None:
            for product in self.imported_file:
                try:
                    if (product["product_name"] #product.get("product_name")
                            and product["nutrition_grades"]
                            and product["stores"]
                            and product["categories"]
                            and product["url"]):
                        new_name = self.cleaner_mono_entry(product["product_name"])
                        new_nutrition_grades = self.cleaner_mono_entry(product["nutrition_grades"])
                        new_stores = self.cleaner_mono_entry(product["stores"])
                        new_categories = self.cleaner_multiples_entry(product["categories"])
                        new_url = product["url"]
                        self.cleaned_list.append({"name":new_name,
                                                  "nutriscore":new_nutrition_grades,
                                                  "store": new_stores,
                                                  "categories": new_categories,
                                                  "url": new_url})

                except KeyError:
                    pass

    def get_cleaned_list(self):
        return self.cleaned_list
    # en minuscule
    # en liste
    # exporter chacun en SQL



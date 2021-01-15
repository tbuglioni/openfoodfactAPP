import requests


class ImportApi:
    """ import french products from api openfoodfact"""

    def __init__(self):
        self.page = None
        self.page_size = None
        self.actual_request = None
        self.status_code = None
        self.imported_file = None

    def api_parameters(self, nbr_page=1, size_page=1000):
        """ define number of page and products to import"""
        self.page = nbr_page
        self.page_size = size_page

    def get_status_code(self):
        """ get the status code from de request api"""
        return self.status_code

    def api_connexion(self):
        """ create the connexion with the api"""
        try:
            payload = {
                "action": "process",
                "sort_by": "unique_scans_n",
                "page_size": self.page_size,
                "page": self.page,
                "json": 1,
            }
            self.actual_request = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
            )
            self.status_code = self.actual_request.status_code
        except requests.exceptions.ConnectionError:
            print(
                "connexion : Ooops there some troubles with the app, check internet connexion please"
            )

    def import_products(self):
        """ import products from the api if connexion is OK"""
        if self.status_code == 200:
            results = self.actual_request.json()
            products = results["products"]
            self.imported_file = products
            return self.imported_file
        else:
            print("get file : there no file to get, status code : ", self.status_code)

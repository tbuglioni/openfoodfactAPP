import requests


class ImportApi:
    def __init__(self):
        self.page = 1
        self.page_size = 100
        self.actual_request = 0
        self.status_code = 0

    def api_parameters(self, nbr_page=1, size_page=100):
        self.page = nbr_page
        self.page_size = size_page

    def api_connexion(self):
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
        except:
            print(
                "connexion : Ooops there some troubles with the app, check internet connexion please"
            )

    def get_product(self):
        if self.status_code == 200:
            results = self.actual_request.json()
            products = results["products"]
            return products
        else:
            print("get file : there no file to get, status code : ", self.status_code)

### independant test section

test = ImportApi()
test.api_parameters()
test.api_connexion()
test.get_product()
### test = ok

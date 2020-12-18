import mysql.connector
import dotenv
import os
dotenv.load_dotenv()


class CreateDb:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user=os.getenv("USER_DB"),
            passwd=os.getenv("PASSWORD_DB"))

    def create_db(self):
        try:
            mycursor = self.db.cursor()
            mycursor.execute("DROP DATABASE IF EXISTS openfoodfact")
            mycursor.execute("CREATE DATABASE openfoodfact")
        except:
            print(
                "trouble : no connexion with MySQL please check MySQL on your computer"
            )


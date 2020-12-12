import mysql.connector
import dotenv
import os
dotenv.load_dotenv()


class CreateDb:
    """
    Create new database with SQL and mysql.connector
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user=os.getenv("USER_DB"),
            passwd=os.getenv("PASSWORD_DB"))
        self.mycursor = self.db.cursor()

    def create_db(self):
        try:
            self.mycursor.execute("DROP DATABASE IF EXISTS openfoodfact")
            self.mycursor.execute("CREATE DATABASE openfoodfact")
        except:
            print(
                "trouble : no connexion with MySQL please check MySQL on your computer"
            )


### independant test section
test = CreateDb()
test.create_db()
### test = ok

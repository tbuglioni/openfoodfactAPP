import mysql.connector
import dotenv
import os

dotenv.load_dotenv()


class CreateDb:
    """ create database """

    def __init__(self):
        self._db = mysql.connector.connect(
            host="localhost",
            user=os.getenv("USER_DB"),
            passwd=os.getenv("PASSWORD_DB")
        )

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, new_value):
        self._db = new_value

    def create_db(self):
        """ create database if not exist """
        try:
            mycursor = self.db.cursor()
            mycursor.execute("CREATE DATABASE IF NOT EXISTS openfoodfact")
        except mysql.connector.Error:
            print(
                "trouble : no connexion with MySQL please check "
                "MySQL on your computer"
            )

    def recreate_db(self):
        """ delete and create database"""
        try:
            mycursor = self.db.cursor()
            mycursor.execute("DROP DATABASE IF EXISTS openfoodfact")
            mycursor.execute("CREATE DATABASE openfoodfact")
        except mysql.connector.Error:
            print(
                "trouble : "
                "no connexion with MySQL please check MySQL on your computer"
            )

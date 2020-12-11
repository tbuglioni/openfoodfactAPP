from peewee import *
import constante
from datetime import date

mysql_db = MySQLDatabase(
    "openfoodfact",
    user=constante.user_db,
    password=constante.password_db,
    host="localhost",
)


class Database(Model):
    class Meta:
        database = mysql_db  # This model uses the "people.db" database.
        id = AutoField(primary_key=True, unique=True)

import mysql.connector
import constante

db = mysql.connector.connect(
    host="localhost",
    user=constante.user_db,
    passwd=constante.password_db,
)

mycursor = db.cursor()
try:
    mycursor.execute("CREATE DATABASE IF NOT EXISTS openfoodfact")
except:
    pass

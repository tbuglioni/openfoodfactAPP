import dotenv
import os

dotenv.load_dotenv()

# database MySQL(local)
user_db = os.getenv("USER_DB")
password_db = os.getenv("PASSWORD_DB")

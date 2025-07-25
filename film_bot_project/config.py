import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "db": os.getenv("MYSQL_DATABASE"),
    "charset": "utf8mb4",
    "cursorclass": __import__('pymysql.cursors').cursors.DictCursor
}

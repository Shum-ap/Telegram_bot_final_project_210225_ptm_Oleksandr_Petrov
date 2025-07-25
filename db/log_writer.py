import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Загружаем .env
load_dotenv()

# Чтение переменных из .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# Инициализация клиента MongoDB
mongo_client = MongoClient(MONGO_URI)
mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]

# 🔧 Логирование в MongoDB
def log_search_to_mongo(user_id, query):
    timestamp = datetime.datetime.now()
    log_entry = {
        "user_id": user_id,
        "query": query,
        "timestamp": timestamp
    }
    mongo_collection.insert_one(log_entry)

# 📝 Дополнительно — логирование в текстовый файл (по желанию)
def log_search(user_id, query):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "search_log.txt")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User {user_id}: {query}\n")

    # Одновременно логируем и в Mongo
    log_search_to_mongo(user_id, query)

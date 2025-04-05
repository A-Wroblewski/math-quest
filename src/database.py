import os

import pymongo
from dotenv import load_dotenv


def connect_to_database():
    connection_string = f"mongodb+srv://{database_username}:{database_password}@cluster0.i2hcdc6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    return pymongo.MongoClient(connection_string)


def get_users_collection(mongo_client):
    users_database = mongo_client["users"]

    return users_database["users"]


load_dotenv()

database_username = os.getenv("DB_USERNAME")
database_password = os.getenv("DB_PASSWORD")

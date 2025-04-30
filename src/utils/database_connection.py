import os

import pymongo
from dotenv import load_dotenv


def connect_to_database():
    connection_string = f"mongodb+srv://{database_username}:{database_password}@cluster0.i2hcdc6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    return pymongo.MongoClient(connection_string)


def get_users_collection(mongo_client):
    users_database = mongo_client["users"]

    return users_database["users"]


def get_math_database(mongo_client):
    return mongo_client["math_questions"]


def get_addition_collection(mongo_client):
    math_database = get_math_database(mongo_client)

    return math_database["addition"]


def get_division_collection(mongo_client):
    math_database = get_math_database(mongo_client)

    return math_database["division"]


def get_multiplication_collection(mongo_client):
    math_database = get_math_database(mongo_client)

    return math_database["multiplication"]


def get_subtraction_collection(mongo_client):
    math_database = get_math_database(mongo_client)

    return math_database["subtraction"]


load_dotenv()

database_username = os.getenv("DB_USERNAME")
database_password = os.getenv("DB_PASSWORD")

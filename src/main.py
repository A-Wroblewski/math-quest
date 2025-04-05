from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo import ReturnDocument

from database import connect_to_database, get_users_collection
from models.user import UserCreate, UserUpdate

app = FastAPI()

mongo_client = connect_to_database()
users_collection = get_users_collection(mongo_client)


@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = users_collection.find_one(ObjectId(user_id))

    if user:
        user["_id"] = str(user["_id"])

        return user

    return HTTPException(404, "User not found")


@app.post("/users")
def create_user(user: UserCreate):
    user_dictionary = user.model_dump()

    users_collection.insert_one(user_dictionary)

    user_dictionary["_id"] = str(user_dictionary["_id"])

    return user_dictionary


@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: UserUpdate):
    query_filter = {"_id": ObjectId(user_id)}

    updated_data = updated_user.model_dump(exclude_unset=True)

    update_operation = {"$set": updated_data}

    updated_document = users_collection.find_one_and_update(
        query_filter, update_operation, return_document=ReturnDocument.AFTER
    )

    if not updated_document:
        return HTTPException(404, "User not found")

    updated_document["_id"] = str(updated_document["_id"])

    return updated_document


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    query_filter = {"_id": ObjectId(user_id)}

    deleted_document = users_collection.find_one_and_delete(query_filter)

    if not deleted_document:
        return HTTPException(404, "User not found")

    deleted_document["_id"] = str(deleted_document["_id"])

    return deleted_document

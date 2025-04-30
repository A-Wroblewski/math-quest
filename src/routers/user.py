import bcrypt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from schemas.user import UserCreate, UserResponse, UserUpdate
from utils.database_connection import connect_to_database, get_users_collection

router = APIRouter(prefix="/users", tags=["users"])

mongo_client = connect_to_database()
users_collection = get_users_collection(mongo_client)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        user = users_collection.find_one(ObjectId(user_id))
    except InvalidId:
        raise HTTPException(400, "Invalid UID format")

    if user:
        user["_id"] = str(user["_id"])

        user.pop("password", None)

        return user

    raise HTTPException(404, "User not found")


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_dictionary = user.model_dump()

    query_filter = {"email": user_dictionary["email"]}

    email_already_registered = users_collection.find_one(query_filter)

    if email_already_registered:
        raise HTTPException(409, "E-mail already registered")

    if user_dictionary["password"] != user_dictionary["confirm_password"]:
        raise HTTPException(400, "Passwords do not match")

    del user_dictionary["confirm_password"]

    hashed_password = bcrypt.hashpw(user_dictionary["password"].encode("utf-8"), bcrypt.gensalt())

    user_dictionary["password"] = hashed_password.decode("utf-8")

    users_collection.insert_one(user_dictionary)

    user_dictionary["_id"] = str(user_dictionary["_id"])

    user_dictionary.pop("password", None)

    return user_dictionary


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_user: UserUpdate):
    try:
        query_filter = {"_id": ObjectId(user_id)}
    except InvalidId:
        raise HTTPException(400, "Invalid UID format")

    updated_data = updated_user.model_dump(exclude_unset=True)

    if "email" in updated_data:
        email_filter = {"email": updated_data["email"]}

        email_already_registered = users_collection.find_one(email_filter)

        if email_already_registered:
            raise HTTPException(409, "E-mail already registered")

    if "password" in updated_data:
        if "confirm_password" in updated_data:
            if updated_data["password"] != updated_data["confirm_password"]:
                raise HTTPException(400, "Passwords do not match")

            del updated_data["confirm_password"]

            updated_data["password"] = bcrypt.hashpw(
                updated_data["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        else:
            raise HTTPException(400, "Missing confirm password field")

    update_operation = {"$set": updated_data}

    updated_document = users_collection.find_one_and_update(
        query_filter, update_operation, return_document=ReturnDocument.AFTER
    )

    if not updated_document:
        raise HTTPException(404, "User not found")

    updated_document["_id"] = str(updated_document["_id"])

    updated_document.pop("password", None)

    return updated_document


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: str):
    try:
        query_filter = {"_id": ObjectId(user_id)}
    except InvalidId:
        raise HTTPException(400, "Invalid UID format")

    deleted_document = users_collection.find_one_and_delete(query_filter)

    if not deleted_document:
        raise HTTPException(404, "User not found")

    deleted_document["_id"] = str(deleted_document["_id"])

    deleted_document.pop("password", None)

    return deleted_document

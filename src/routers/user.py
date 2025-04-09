from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from schemas.user import UserCreate, UserResponse, UserUpdate
from utils.database_connection import connect_to_database, get_users_collection

router = APIRouter(prefix="/users", tags=["users"])

mongo_client = connect_to_database()
users_collection = get_users_collection(mongo_client)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = users_collection.find_one(ObjectId(user_id))

    if user:
        user["_id"] = str(user["_id"])

        return user

    raise HTTPException(404, "User not found")


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_dictionary = user.model_dump()

    query_filter = {"email": user_dictionary["email"]}

    email_already_registered = users_collection.find_one(query_filter)

    if email_already_registered:
        raise HTTPException(409, "E-mail already registered")

    users_collection.insert_one(user_dictionary)

    user_dictionary["_id"] = str(user_dictionary["_id"])

    return user_dictionary


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_user: UserUpdate):
    query_filter = {"_id": ObjectId(user_id)}

    updated_data = updated_user.model_dump(exclude_unset=True)

    update_operation = {"$set": updated_data}

    updated_document = users_collection.find_one_and_update(
        query_filter, update_operation, return_document=ReturnDocument.AFTER
    )

    if not updated_document:
        raise HTTPException(404, "User not found")

    updated_document["_id"] = str(updated_document["_id"])

    return updated_document


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: str):
    query_filter = {"_id": ObjectId(user_id)}

    deleted_document = users_collection.find_one_and_delete(query_filter)

    if not deleted_document:
        raise HTTPException(404, "User not found")

    deleted_document["_id"] = str(deleted_document["_id"])

    return deleted_document

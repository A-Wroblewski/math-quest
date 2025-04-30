from fastapi import APIRouter

from schemas.math import EquationResponse
from utils.database_connection import (
    connect_to_database,
    get_addition_collection,
    get_division_collection,
    get_math_database,
    get_multiplication_collection,
    get_subtraction_collection,
)

router = APIRouter(prefix="/math", tags=["math"])

mongo_client = connect_to_database()
math_database = get_math_database(mongo_client)

addition_collection = get_addition_collection(math_database)
division_collection = get_division_collection(math_database)
multiplication_collection = get_multiplication_collection(math_database)
subtraction_collection = get_subtraction_collection(math_database)


@router.get("/addition", response_model=EquationResponse)
def get_addition_equation():
    pipeline = [{"$sample": {"size": 1}}, {"$project": {"_id": 0}}]

    return addition_collection.aggregate(pipeline).next()


@router.get("/division", response_model=EquationResponse)
def get_division_equation():
    pipeline = [{"$sample": {"size": 1}}, {"$project": {"_id": 0}}]

    return division_collection.aggregate(pipeline).next()


@router.get("/multiplication", response_model=EquationResponse)
def get_multiplication_equation():
    pipeline = [{"$sample": {"size": 1}}, {"$project": {"_id": 0}}]

    return multiplication_collection.aggregate(pipeline).next()


@router.get("/subtraction", response_model=EquationResponse)
def get_subtraction_equation():
    pipeline = [{"$sample": {"size": 1}}, {"$project": {"_id": 0}}]

    return subtraction_collection.aggregate(pipeline).next()

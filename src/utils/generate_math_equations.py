from database_connection import (
    connect_to_database,
    get_addition_collection,
    get_division_collection,
    get_math_database,
    get_multiplication_collection,
    get_subtraction_collection,
)

mongo_client = connect_to_database()
math_database = get_math_database(mongo_client)

addition_collection = get_addition_collection(math_database)
division_collection = get_division_collection(math_database)
multiplication_collection = get_multiplication_collection(math_database)
subtraction_collection = get_subtraction_collection(math_database)


def generate_addition_equations():
    for first_value in range(101):
        for second_value in range(101):
            if first_value + second_value <= 100:
                equation = f"{first_value} + {second_value} ="
                result = first_value + second_value

                if not addition_collection.find_one({"equation": equation}):
                    addition_collection.insert_one({"equation": equation, "result": result})


def generate_division_equations():
    for divisor in range(1, 11):
        for result in range(1, 11):
            dividend = divisor * result

            equation = f"{dividend} / {divisor} ="
            result = dividend / divisor

            if not division_collection.find_one({"equation": equation}):
                division_collection.insert_one({"equation": equation, "result": result})


def generate_multiplication_equations():
    for first_value in range(1, 11):
        for second_value in range(1, 11):
            equation = f"{first_value} * {second_value} ="
            result = first_value * second_value

            if not multiplication_collection.find_one({"equation": equation}):
                multiplication_collection.insert_one({"equation": equation, "result": result})


def generate_subtraction_equations():
    for first_value in range(101):
        for second_value in range(101):
            if first_value >= second_value:
                equation = f"{first_value} - {second_value} ="
                result = first_value - second_value

                if not subtraction_collection.find_one({"equation": equation}):
                    subtraction_collection.insert_one({"equation": equation, "result": result})


generate_addition_equations()
generate_division_equations()
generate_multiplication_equations()
generate_subtraction_equations()

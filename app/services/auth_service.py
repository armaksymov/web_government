"""
This module contains the implementation for the user authentication
on login as well the user registration
"""
import re
import bcrypt
from flask import current_app
import random
import string
import datetime


def is_valid_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


def authenticate_user(email, password):
    """
    Authenticate a user by email and password

    Args:
    - email (string)
    - password(string)

    Returns:
    - dict: the authentication status and the user ID if successful
    """

    if not email or not password:
        return {"status": 2}  # status 2 : missing email or passwword

    if not is_valid_email(email):
        return {"status": 3}  # status 3 : invalid email format

    users_collection = current_app.mongo.db.users
    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return {"status": 0, "id": str(user["_id"])}

    return {"status": 1, "id": None}

def generate_random_data():
   
    random_data= {
        "passport_number": "P" + ''.join(random.choices(string.digits, k=9)),
        "driver_license":''.join(random.choices(string.digits, k=9))
    }
    return random_data

def generate_random_document_data(full_name):
    """
    Generate the data for the documents

    Args:
    -full_name (str)

    Returns:
    -dict: the generated data
    """

    random_date = lambda start_year,end_year: str(datetime.date(
        random.randint(start_year,end_year),
        random.randint(1,12),
        random.randint(1,28)
    ))

    return{
        "passport": {
            "number": "P" + ''.join(random.choices(string.digits, k=9)),
            "full_name": full_name,
            "place_of_birth": "Essex",
            "date_of_birth": random_date(1960, 2024),
            "date_of_issue": random_date(2014, 2024),
            "date_of_expiry": random_date(2020, 2034),
            "issuing_authority": "Sussex Passport Office",
        },
        "driver_license": {
            "number": ''.join(random.choices(string.digits, k=9)),
            "full_name": full_name,
            "date_of_birth": random_date(1960, 2024),
            "date_of_issue": random_date(2010, 2024),
            "date_of_expiry": random_date(2020, 2034),
            "sex": random.choice(["Male", "Female"]),
            "blood_type": random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            "weight": random.randint(50, 100),
        }

    }

    

def register_user(first_name, last_name, email, password):
    """
    Register a new user

    Args:
    - first name(string)
    - last name (string)
    - email (string)
    - password(string)

    Returns:
    - dict: status of the registration and user ID if successful
    """

    if not all([first_name, last_name, email, password]):
        return {"status": 2}  # status 2: missing fields

    if not is_valid_email(email):
        return {"status": 3}  # status 3 : invalid email format

    users_collection = current_app.mongo.db.users

    if users_collection.find_one({"email": email}):
        return {"status": 4, "id": None}  # status 4: email already exist

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_account = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password,
    }

    try:
        user_id = users_collection.insert_one(user_account).inserted_id
        return {"status": 0, "id": str(user_id)}
    except Exception:
        return {"status": 5, "id": None}  # registration error

"""
This module contains the implementation for the user authentication
on login as well the user registration
"""
from __future__ import annotations

import re
import string
from faker import Faker
import random
import datetime

import bcrypt
from flask import current_app
from datetime import timedelta
import logging

fake = Faker()


def is_valid_email(email):
    """
    Email validation against the standard email regex

    Args:
    - email (string)

    Returns:
    - boolean: the boolean value representing the regex match
    """

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


def random_date(start_age, end_age):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=end_age * 365)
    end_date = today - datetime.timedelta(days=start_age * 365)
    return fake.date_of_birth(
        tzinfo=None, minimum_age=start_age, maximum_age=end_age
    ).strftime("%Y-%m-%d")


def generate_passport_data(passport_number, full_name, date_of_birth, blood_type):
    return {
        "number": passport_number,
        "full_name": full_name,
        "place_of_birth": fake.city(),
        "date_of_birth": date_of_birth,
        "date_of_issue": fake.date_this_decade().strftime("%Y-%m-%d"),
        "date_of_expiry": (
            datetime.date.today() + datetime.timedelta(days=365 * 10)
        ).strftime("%Y-%m-%d"),
        "issuing_authority": fake.random_element(
            elements=(
                "US Passport Agency",
                "UK Passport Office",
                "Canada Passport Office",
            )
        ),
        "blood_type": blood_type,
    }


def generate_driver_license_data(
    driver_license_number, full_name, date_of_birth, blood_type
):
    return {
        "number": driver_license_number,
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "date_of_issue": fake.date_this_decade().strftime("%Y-%m-%d"),
        "date_of_expiry": (
            datetime.date.today() + datetime.timedelta(days=365 * 10)
        ).strftime("%Y-%m-%d"),
        "sex": fake.random_element(elements=("Male", "Female")),
        "blood_type": blood_type,
        "weight": fake.random_int(min=50, max=100),
    }


def generate_health_card_data(health_card_number, full_name, date_of_birth, blood_type):
    return {
        "number": health_card_number,
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "date_of_issue": fake.date_this_decade().strftime("%Y-%m-%d"),
        "insurance_provider": fake.company(),
        "policy_number": fake.random_int(min=10000, max=99999),
        "blood_type": blood_type,
        "covid_vaccination_status": fake.random_element(
            elements=("Fully Vaccinated", "Partially Vaccinated", "Not Vaccinated")
        ),
    }


def generate_random_document_data(
    full_name, passport_number, driver_license_number, health_card_number
):
    """
    Generate random data for passport, driver license, and health card.

    Returns:
    - dict: The generated data for passport, driver license, and health card
    """

    # Generate common data
    common_data = {
        "full_name": full_name,
        "date_of_birth": random_date(18, 80),
        "blood_type": fake.random_element(
            elements=("A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")
        ),
    }

    # Generate individual data
    passport_data = generate_passport_data(passport_number, **common_data)
    driver_license_data = generate_driver_license_data(
        driver_license_number, **common_data
    )
    health_card_data = generate_health_card_data(health_card_number, **common_data)

    # Return combined data
    return {
        "passport": passport_data,
        "driver_license": driver_license_data,
        "health_card": health_card_data,
    }

def generate_random_bills_data(account_id):
      # Generate expiry date
    expiry_date = fake.date_between(start_date="today", end_date="+365d")

    # Generate issuance date before expiry date
    issuance_date = fake.date_between(
        start_date="-365d", end_date=expiry_date - timedelta(days=1)
    )

    # Generate renewal deadline after expiry date
    renewal_deadline = fake.date_between(
        start_date=expiry_date + timedelta(days=1),
        end_date=expiry_date + timedelta(days=30),
    )

    # Generate renewal period based on expiry date
    renewal_period = fake.random_element(elements=("1 year", "2 years", "3 years"))

    # Adjust fee range based on renewal period
    if renewal_period == "1 year":
        min_fee, max_fee = 50, 100
    elif renewal_period == "2 years":
        min_fee, max_fee = 100, 150
    else:
        min_fee, max_fee = 150, 200


    bills = {
        "user_id": account_id,
        "electricity": {
            "number": fake.random_number(digits=9),
            "due": fake.date_between(start_date="today", end_date="+30d").strftime(
                "%d %b %Y"
            ),
            "issued": fake.date_between(start_date="-30d", end_date="today").strftime(
                "%d %b %Y"
            ),
            "amount": "{:.2f}".format(
                fake.pydecimal(
                    left_digits=2,
                    right_digits=2,
                    positive=True,
                    min_value=40,
                    max_value=80,
                )
            ),
            "is_paid": False,
        },
        "internet_and_cable": {
            "number": fake.random_number(digits=9),
            "due": fake.date_between(start_date="today", end_date="+30d").strftime(
                "%d %b %Y"
            ),
            "issued": fake.date_between(start_date="-30d", end_date="today").strftime(
                "%d %b %Y"
            ),
            "amount": "{:.2f}".format(
                fake.pydecimal(
                    left_digits=2,
                    right_digits=2,
                    positive=True,
                    min_value=40,
                    max_value=80,
                )
            ),
            "is_paid": False,
        },
        "property_tax":{
            "number": fake.random_number(digits=9),
        "issued": fake.date_between(start_date="-30d", end_date="today").strftime(
            "%d %b %Y"
        ),
        "due": fake.date_between(start_date="today", end_date="+30d").strftime(
            "%d %b %Y"
        ),
        "tax_rate": fake.pyfloat(
            left_digits=1, right_digits=2, positive=True, min_value=1, max_value=3
        ),
        "value": fake.random_number(digits=6),
        "is_paid": False,
        },
        "license": {
            "number": fake.random_number(digits=9),
            "is_paid": False,
            "expiry_date": expiry_date.strftime("%d %b %Y"),
            "renewal_fee": round(
                fake.pyfloat(
                    left_digits=3,
                    right_digits=2,
                    positive=True,
                    min_value=min_fee,
                    max_value=max_fee,
                ),
                -1,
            ),
            "renewal_period": renewal_period,
            "renewal_deadline": renewal_deadline.strftime("%d %b %Y"),
        },
        "registration": {
            "number": fake.random_number(digits=9),
            "is_paid": False,
            "make": fake.company(),
            "year": fake.year(),
            "plate_number": "".join(fake.random_letters(length=3)).upper()
            + str(fake.random_int(min=1000, max=9999)),
            "expiry_date": expiry_date.strftime("%d %b %Y"),
            "renewal_fee": round(
                fake.pyfloat(
                    left_digits=3,
                    right_digits=2,
                    positive=True,
                    min_value=min_fee,
                    max_value=max_fee,
                ),
                -1,
            ),
            "renewal_period": renewal_period,
            "renewal_deadline": renewal_deadline.strftime("%d %b %Y"),
        },
        }
    return bills
    



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
        logging.error("Missing registration fields")
        return {"status": 2}  # status 2: missing fields

    if not is_valid_email(email):
        logging.error("Invalid email format: {}".format(email))
        return {"status": 3}  # status 3: invalid email format

    users_collection = current_app.mongo.db.users

    if users_collection.find_one({"email": email}):
        logging.error("Email already exists: {}".format(email))
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
        logging.info("User account created successfully: {}".format(user_id))
    except Exception as e:
        logging.error("Error in creating user account: {}".format(e))
        return {"status": 5, "id": None}  # registration error

    try:
        utility_bills_data = generate_random_bills_data(str(user_id))

        logging.debug("Type of utility_bills_data: {}".format(type(utility_bills_data)))
        logging.debug("Content of utility_bills_data: {}".format(utility_bills_data))

        bills_collection = current_app.mongo.db.bills
        bills_collection.insert_one(utility_bills_data)
        logging.info("Bills data inserted successfully for user_id: {}".format(user_id))
    except Exception as e:
        logging.error("Error in inserting bills data: {}".format(e))
        return {"status": 5, "id": None}  # registration error


    passport_number = "P" + "".join(random.choices(string.digits, k=9))
    driver_license_number = "".join(random.choices(string.digits, k=9))
    health_card_number = "".join(random.choices(string.digits, k=9))

    user_details = {
        "user_id": str(user_id),
        "passport_number": passport_number,
        "driver_license_number": driver_license_number,
        "health_card_number": health_card_number,
    }

    full_name = f"{first_name} {last_name}"
    document_data = generate_random_document_data(
        full_name, passport_number, driver_license_number, health_card_number
    )
    document_data["user_id"] = str(user_id)

    user_details_collection = current_app.mongo.db.user_details
    documents_collection = current_app.mongo.db.documents

    try:
        user_details_collection.insert_one(user_details)
        documents_collection.insert_one(document_data)
        logging.info("User details and documents inserted successfully for user_id: {}".format(user_id))
    except Exception as e:
        users_collection.delete_one({"_id": user_id})
        logging.error("Error in inserting user details/documents, rollback initiated: {}".format(e))
        return {"status": 6, "id": None}  # error inserting user details

    return {"status": 0, "id": str(user_id)}

def change_password(user_id, old_password, new_password):
    users_collection = current_app.mongo.db.users
    user = users_collection.find_one({"_id":user_id})

    if user is None:
        return {"status":2,"message":"User not Found"}
    
    if not bcrypt.checkpw(old_password.encode('utf-8'),user['password']):
        return {"status":3,"message": "Incorrect Old Password"}
    
    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())

    users_collection.update_one(
        {"_id":user_id},
        {"$set":{"password":hashed_new_password}}
    )

    return {"status":0,"message":"Password changed successfully"}



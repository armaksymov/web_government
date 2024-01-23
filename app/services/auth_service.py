"""
This module contains the implementation for the user authentication
on login as well the user registration
"""
from __future__ import annotations

import datetime
import random
import re
import string

import bcrypt
from flask import current_app


def is_valid_email(email):
    """
    Email validation against the standard email regex

    Args:
    - email (string)

    Returns:
    - boolean: the boolean value representing the regex match
    """

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
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
        return {'status': 2}  # status 2 : missing email or passwword

    if not is_valid_email(email):
        return {'status': 3}  # status 3 : invalid email format

    users_collection = current_app.mongo.db.users
    user = users_collection.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return {'status': 0, 'id': str(user['_id'])}

    return {'status': 1, 'id': None}


def generate_random_document_data(full_name, passport_number, driver_license_number):
    """
    Generate the data for the documents

    Args:
    -full_name (str)

    Returns:
    -dict: the generated data
    """

    def random_date(start_year, end_year):
        return str(
            datetime.date(
                random.randint(start_year, end_year),
                random.randint(1, 12),
                random.randint(1, 28),
            ),
        )

    return {
        'passport': {
            'number': passport_number,
            'full_name': full_name,
            'place_of_birth': 'Essex',
            'date_of_birth': random_date(1960, 2024),
            'date_of_issue': random_date(2014, 2024),
            'date_of_expiry': random_date(2020, 2034),
            'issuing_authority': 'Sussex Passport Office',
        },
        'driver_license': {
            'number': driver_license_number,
            'full_name': full_name,
            'date_of_birth': random_date(1960, 2024),
            'date_of_issue': random_date(2010, 2024),
            'date_of_expiry': random_date(2020, 2034),
            'sex': random.choice(['Male', 'Female']),
            'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
            'weight': random.randint(50, 100),
        },

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
        return {'status': 2}  # status 2: missing fields

    if not is_valid_email(email):
        return {'status': 3}  # status 3 : invalid email format

    users_collection = current_app.mongo.db.users

    if users_collection.find_one({'email': email}):
        return {'status': 4, 'id': None}  # status 4: email already exist

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_account = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
    }

    try:
        user_id = users_collection.insert_one(user_account).inserted_id
    except Exception:
        return {'status': 5, 'id': None}  # registration error

    passport_number = 'P' + ''.join(random.choices(string.digits, k=9))
    driver_license_number = ''.join(random.choices(string.digits, k=9))

    user_details = {
        'user_id': str(user_id),
        'passport_number': passport_number,
        'driver_license_number': driver_license_number,
    }

    full_name = f"{first_name} {last_name}"
    document_data = generate_random_document_data(
        full_name, passport_number, driver_license_number,
    )
    # link the documents data to each user
    document_data['user_id'] = str(user_id)

    user_details_collection = current_app.mongo.db.user_details
    documents_collection = current_app.mongo.db.documents

    try:
        user_details_collection.insert_one(user_details)
        documents_collection.insert_one(document_data)
    except Exception:
        # roll back if details or documents insertion is failed
        users_collection.delete_one({'_id': user_id})
        return {'status': 6, 'id': None}  # error inserting user details

    return {'status': 0, 'id': str(user_id)}

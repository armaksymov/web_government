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
from faker import Faker
from flask import current_app

fake = Faker()


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


def random_date(start_age, end_age):
    """
        A method to generate a random date of birth for documents
    """

    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=end_age * 365)
    end_date = today - datetime.timedelta(days=start_age * 365)
    return fake.date_of_birth(
        tzinfo=None, minimum_age=start_age, maximum_age=end_age,
    ).strftime('%Y-%m-%d')


def generate_passport_data(passport_number, full_name, date_of_birth, blood_type):
    """
        A method to generate random passport data based on passed parameters:
            1. Passport Number
            2. Full Name
            3. Date of birth
            4. Blood type
    """

    return {
        'number': passport_number,
        'full_name': full_name,
        'place_of_birth': fake.city(),
        'date_of_birth': date_of_birth,
        'date_of_issue': fake.date_this_decade().strftime('%Y-%m-%d'),
        'date_of_expiry': (
            datetime.date.today() + datetime.timedelta(days=365 * 10)
        ).strftime('%Y-%m-%d'),
        'issuing_authority': fake.random_element(
            elements=(
                'US Passport Agency',
                'UK Passport Office',
                'Canada Passport Office',
            ),
        ),
        'blood_type': blood_type,
    }


def generate_driver_license_data(
    driver_license_number, full_name, date_of_birth, blood_type,
):
    """
        A method to generate random driver's liccense data based on passed arguments:
            1. Driver's License Number
            2. Full Name
            3. Date of birth
            4. Blood type
    """

    return {
        'number': driver_license_number,
        'full_name': full_name,
        'date_of_birth': date_of_birth,
        'date_of_issue': fake.date_this_decade().strftime('%Y-%m-%d'),
        'date_of_expiry': (
            datetime.date.today() + datetime.timedelta(days=365 * 10)
        ).strftime('%Y-%m-%d'),
        'sex': fake.random_element(elements=('Male', 'Female')),
        'blood_type': blood_type,
        'weight': fake.random_int(min=50, max=100),
    }


def generate_health_card_data(health_card_number, full_name, date_of_birth, blood_type):
    """
        A method to generate a randomdata for user's health card.
        Generates the card based on the passed arguments:
            1. Driver's License Number
            2. Full Name
            3. Date of birth
            4. Blood type
    """

    return {
        'number': health_card_number,
        'full_name': full_name,
        'date_of_birth': date_of_birth,
        'date_of_issue': fake.date_this_decade().strftime('%Y-%m-%d'),
        'insurance_provider': fake.company(),
        'policy_number': fake.random_int(min=10000, max=99999),
        'blood_type': blood_type,
        'covid_vaccination_status': fake.random_element(
            elements=(
                'Fully Vaccinated',
                'Partially Vaccinated', 'Not Vaccinated',
            ),
        ),
    }


def generate_random_document_data(
    full_name, passport_number, driver_license_number, health_card_number,
):
    """
    Generate random data for passport, driver license, and health card.

    Returns:
    - dict: The generated data for passport, driver license, and health card
    """

    # Generate common data
    common_data = {
        'full_name': full_name,
        'date_of_birth': random_date(18, 80),
        'blood_type': fake.random_element(
            elements=('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'),
        ),
    }

    # Generate individual data
    passport_data = generate_passport_data(passport_number, **common_data)
    driver_license_data = generate_driver_license_data(
        driver_license_number, **common_data,
    )
    health_card_data = generate_health_card_data(
        health_card_number, **common_data,
    )

    # Return combined data
    return {
        'passport': passport_data,
        'driver_license': driver_license_data,
        'health_card': health_card_data,
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
    health_card_number = ''.join(random.choices(string.digits, k=9))

    user_details = {
        'user_id': str(user_id),
        'passport_number': passport_number,
        'driver_license_number': driver_license_number,
        'health_card_number': health_card_number,
    }

    full_name = f"{first_name} {last_name}"
    document_data = generate_random_document_data(
        full_name, passport_number, driver_license_number, health_card_number,
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

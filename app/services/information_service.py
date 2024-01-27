"""
    This module contains methods to request data from the database.
"""
from __future__ import annotations

import logging

from bson import ObjectId
from flask import current_app
from faker import Faker
from datetime import timedelta

fake = Faker()


def renew_license(account_id):
    response = {
        "status": 0,
    }

    return response


def get_license_and_registration(account_id):
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

    license_and_registration = {
        "license": {
            "number": fake.random_number(digits=9),
            "is_paid": fake.boolean(),
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
        }
    }

    return license_and_registration


def get_property_taxes(account_id):
    property_taxes = {
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
        "is_paid": fake.boolean(),
    }

    return property_taxes


def pay_property_tax(account_id):
    response = {
        "status": 0,
    }

    return response


def get_utility_bills(account_id):
    """
    This method get_utility_bills returns a dictionary with bill information

    Arguments:
    1. account_id - Unique Internal Client Identifier within our system

    Returns:
    1. A dictionary containing data on utility bills.
    """

    bills_collection = current_app.mongo.db.bills

    existing_bills = bills_collection.find_one({"account_id": account_id})
    if existing_bills:
        return existing_bills
    else:
        utility_bills = {
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
    }
        utility_bills['account_id'] = account_id
        bills_collection.insert_one(utility_bills)
        return utility_bills


def pay_utility_bill(account_id, bill_name):
    """
    This method pay_utility_bill returns a status code of bill payment

    Arguments:
    1. account_id - Unique Internal Client Identifier within our system
    2. bill_name - Name of the bill user is paying

    Returns:
    1. A status code reflecting the success of bill payment.
    """

    bills_collection = current_app.mongo.db.bills
    bill_update_result = bills_collection.update_one(
        {"account_id": account_id, bill_name: {"$exists": True}},
        {"$set": {f"{bill_name}.is_paid": True}}
    )

    if bill_update_result.modified_count > 0:
        response = {"status": 0, "id": account_id}  # status 0 indicates success
    else:
        response = {"status": 1, "id": account_id}  # status 1 indicates failure

    return response



def get_account_information(account_id):
    """
    This method get_account_information returns a dictionary with user data

    Arguments:
    1. account_id - Unique Internal Client Identifier within our system

    Returns:
    1. A dictionary with the following user data:
        - Account finding status (0 - success, 1 - not found)
        - First Name
        - Last Name
        - Email Address
    """

    users_collection = current_app.mongo.db.users

    user = users_collection.find_one({"_id": account_id})
    if user:
        account_information = {
            "status": 0,
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
            "email": user.get("email", ""),
        }
    else:
        account_information = {"status": 1}  # not found
    return account_information


def get_documents(account_id):
    """
    This method get_documents returns a dictionary with user documents

    Arguments:
    1. account_id - Unique Internal Client Identifier within our system

    Returns:
    1. A dictionary with the following user documents:
        - Document finding status (0 - success, 1 - not found)
        - Passport
        - Driver's License
    """

    documents_collection = current_app.mongo.db.documents

    if not ObjectId.is_valid(account_id):
        logging.error(f"Invalid account_id format: {account_id}")
        return {"status": 1}

    account_obj_id = ObjectId(account_id)

    doc = documents_collection.find_one(
        {"user_id": str(account_obj_id)},
    )  # get the documents for each user
    if doc:
        documents = {
            "status": 0,
            "passport": doc.get("passport", {}),
            "driver_license": doc.get("driver_license", {}),
            "health_card": doc.get("health_card", {}),
        }
    else:
        logging.error(f"No documents found for user_id: {account_id}")
        documents = {"status": 1}

    return documents


def get_user_data(account_id):
    """
    Retrieve all user data from the database.

    Args:
    - account_id (str): CLIENT ID.

    Returns:
    - dict: basic user data combined with additional user details.
    """
    mongo_db = current_app.mongo

    users_collection = mongo_db.db.users  # get users collection
    basic_info = users_collection.find_one({"_id": account_id})

    user_details_collection = mongo_db.db.user_details  # get users_details collection
    additional_info = user_details_collection.find_one({"user_id": account_id})

    if basic_info and additional_info:
        basic_info.pop("_id", None)
        additional_info.pop("_id", None)
        additional_info.pop("user_id", None)  # remove the user ID

        # merge both information
        user_data = {**basic_info, **additional_info}

        return user_data
    else:
        return {"status": 1}

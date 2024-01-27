"""
    This module contains methods to request data from the database.
"""
from __future__ import annotations

import logging
from datetime import timedelta

from bson import ObjectId
from faker import Faker
from flask import current_app

fake = Faker()


def renew_license(account_id):
    bills_collection = current_app.mongo.db.bills
    new_expiry_date = fake.date_between(start_date="+1y", end_date="+2y").strftime("%d %b %Y")

    update_result = bills_collection.update_one(
        {"user_id": account_id, "license": {"$exists": True}},
        {
            "$set": {
                "license.expiry_date": new_expiry_date,
                "license.is_paid": True
            }
        }
    )

    if update_result.modified_count > 0:
        response = {"status": 0, "id": account_id}  # status 0 indicates success
    else:
        response = {"status": 1, "id": account_id}  # status 1 indicates failure

    return response

def renew_registration(account_id):
    bills_collection = current_app.mongo.db.bills
    new_expiry_date = fake.date_between(start_date="+1y", end_date="+2y").strftime("%d %b %Y")

    update_result = bills_collection.update_one(
        {"user_id": account_id, "registration": {"$exists": True}},
        {
            "$set": {
                "registration.expiry_date": new_expiry_date,
                "registration.is_paid": True
            }
        }
    )

    if update_result.modified_count > 0:
        response = {"status": 0, "id": account_id}  # status 0 indicates success
    else:
        response = {"status": 1, "id": account_id}  # status 1 indicates failure

    return response



def get_license_and_registration(account_id):
    bills_collection = current_app.mongo.db.bills

    existing_records = bills_collection.find_one(
        {"user_id": account_id},
        {"license": 1, "registration": 1, "_id": 0} 
    )

    if existing_records and "license" in existing_records and "registration" in existing_records:
        return {
            "license": existing_records["license"],
            "registration": existing_records["registration"]
        }
    else:
        logging.error(f"No license or registration data found for user_id: {account_id}")
        return {
            "error": "No license or registration data found."
        }




def get_property_taxes(account_id):
    """
        This method get_property_taxes returns a dictionary with property taxes information

        Arguments:
        1. account_id - Unique Internal Client Identifier within our system

        Returns:
        1. A dictionary with containing data on user's property taxes.
    """

    bills_collection = current_app.mongo.db.bills

    existing_bills = bills_collection.find_one({"user_id": account_id})
    if existing_bills and "property_tax" in existing_bills:
        return existing_bills["property_tax"]
   

def pay_property_tax(account_id):
    """
        This method pay_property_tax allows user to "make a payment"
        and update records in the database.

        Arguments:
        1. account_id - Unique Internal Client Identifier within our system

        Returns:
        1. A status code confirming whether the payment went through.
        2. account_id - Unique Internal Client Identifier within our system
    """

    bills_collection = current_app.mongo.db.bills

    bill_update_result = bills_collection.update_one(
        {"user_id": account_id, "property_tax": {"$exists": True}},
        {"$set": {"property_tax.is_paid": True}}
    )

    if bill_update_result.modified_count > 0:
        # status 0 indicates success
        response = {'status': 0, 'id': account_id}
    else:
        # status 1 indicates failure
        response = {'status': 1, 'id': account_id}

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

    existing_bills = bills_collection.find_one({"user_id": account_id})
    if existing_bills:
        return existing_bills
    


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
        {"user_id": account_id, bill_name: {"$exists": True}},
        {"$set": {f"{bill_name}.is_paid": True}}
    )

    if bill_update_result.modified_count > 0:
        # status 0 indicates success
        response = {'status': 0, 'id': account_id}
    else:
        # status 1 indicates failure
        response = {'status': 1, 'id': account_id}

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

    user = users_collection.find_one({'_id': account_id})
    if user:
        account_information = {
            'status': 0,
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'email': user.get('email', ''),
        }
    else:
        account_information = {'status': 1}  # not found
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
        return {'status': 1}

    account_obj_id = ObjectId(account_id)

    doc = documents_collection.find_one(
        {'user_id': str(account_obj_id)},
    )  # get the documents for each user
    if doc:
        documents = {
            'status': 0,
            'passport': doc.get('passport', {}),
            'driver_license': doc.get('driver_license', {}),
            'health_card': doc.get('health_card', {}),
        }
    else:
        logging.error(f"No documents found for user_id: {account_id}")
        documents = {'status': 1}

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
    basic_info = users_collection.find_one({'_id': account_id})

    user_details_collection = mongo_db.db.user_details  # get users_details collection
    additional_info = user_details_collection.find_one({'user_id': account_id})

    if basic_info and additional_info:
        basic_info.pop('_id', None)
        additional_info.pop('_id', None)
        additional_info.pop('user_id', None)  # remove the user ID

        # merge both information
        user_data = {**basic_info, **additional_info}

        return user_data
    else:
        return {'status': 1}

"""
    This module contains methods to request data from the database.
"""
from __future__ import annotations

import logging

from bson import ObjectId
from flask import current_app

def get_property_taxes(account_id):
    property_taxes = {
        'number': '532251286',
        'issued': '01 Jan 2024',
        'due': '10 Jan 2024',
        'tax_rate': '18',
        'value': '64,779',
        'is_paid': False,
        'amount': '6,853'
    }

    return property_taxes

def pay_property_tax(account_id):
    response = {
        'status': 0,
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

    utility_bills = {
        'electricity': {
            'due': '01 Jan 2024',
            'issued': '01 Jan 2024',
            'amount': '62.78',
            'is_paid': False,
        },
        'internet_and_cable': {
            'due': '01 Jan 2024',
            'issued': '01 Jan 2024',
            'amount': '81.83',
            'is_paid': True,
        },
    }

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

    response = {
        'status': 0,
    }

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
            'health_card': doc.get('health_card', {})
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

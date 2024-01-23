from flask import current_app
from bson import ObjectId
import logging


def get_utility_bills(account_id):
    utility_bills = {
        "electricity": {
            "due": "01 Jan 2024",
            "issued": "01 Jan 2024",
            "amount": "62.78",
            "is_paid": False,
        },
        "internet_and_cable": {
            "due": "01 Jan 2024",
            "issued": "01 Jan 2024",
            "amount": "81.83",
            "is_paid": True,
        },
    }

    return utility_bills


def pay_utility_bill(account_id, bill_name):
    return NotImplementedError


def get_account_information(account_id):
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
    documents_collection = current_app.mongo.db.documents

    if not ObjectId.is_valid(account_id):
        logging.error(f"Invalid account_id format: {account_id}")
        return {"status": 1}

    account_obj_id = ObjectId(account_id)

    doc = documents_collection.find_one(
        {"user_id": str(account_obj_id)}
    )  # get the documents for each user
    if doc:
        documents = {
            "status": 0,
            "passport": doc.get("passport", {}),
            "driver_license": doc.get("driver_license", {}),
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

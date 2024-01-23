from flask import current_app
from bson import ObjectId
import logging

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
        account_information = {"status": 1} #not found
    return account_information


def get_documents(account_id):
    documents_collection = current_app.mongo.db.documents

    if not ObjectId.is_valid(account_id):
        logging.error(f"Invalid account_id format: {account_id}")
        return {"status": 1}

    account_obj_id = ObjectId(account_id)

    doc = documents_collection.find_one({"user_id": str(account_obj_id)})#get the documents for each user
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

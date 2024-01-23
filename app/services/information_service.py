from flask import current_app

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
    documents = {
        "status": 0,
        "passport": {
            "number": "P000000000",
            "full_name": "John Doe",
            "place_of_birth": "Cityville",
            "date_of_birth": "01 Jan 1980",
            "date_of_issue": "01 Jan 2020",
            "date_of_expiry": "01 Jan 2030",
            "issuing_authority": "Cityville Passport Office",
        },
        "driver_license": {
            "number": "000000000",
            "full_name": "John Doe",
            "date_of_birth": "01 Jan 1980",
            "date_of_issue": "01 Jan 2010",
            "date_of_expiry": "01 Jan 2030",
            "sex": "Male",
            "blood_type": "O+",
            "weight": 90,
        },
    }

    return documents

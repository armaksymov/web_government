def get_account_information(account_id):
    account_information = {
        "status": 0,
        "first_name": "",
        "last_name": "",
        "email": "",
    }

    return account_information


def get_documents(account_id):
    documents = {
        "status": 0,
        "passport": {
            "number": "",
            "full_name": "",
            "place_of_birth": "",
            "date_of_birth": "",
            "date_of_issue": "",
            "date_of_expiry": "",
            "issuing_authority": "",
        },
        "driver_license": {
            "number": "",
            "full_name": "",
            "date_of_birth": "",
            "date_of_issue": "",
            "date_of_expiry": "",
            "sex": "",
            "blood_type": "",
            "weight": 0,
        },
    }

    return documents

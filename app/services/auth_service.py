from flask import current_app, jsonify
import bcrypt

def authenticate_user(email, password):
    users_collection = current_app.mongo.db.users
    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return {"status": 0, "id": str(user['_id'])}
    else:
        return {"status": 1, "id": None}

def register_user(first_name, last_name, email, password):
    users_collection = current_app.mongo.db.users

    # Check if email already exists
    if users_collection.find_one({"email": email}):
        return {"status": 1, "message": "Email already exists"}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_account = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password
    }

    try:
        user_id = users_collection.insert_one(user_account).inserted_id
        return {"status": 0, "id": str(user_id)}
    except Exception as e:
        return {"status": 1, "message": str(e)}

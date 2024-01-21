"""
This module contains the implementation for the user authentication
on login as well the user registration
"""

from flask import current_app
import bcrypt

def authenticate_user(email, password):
    """
    Authenticate a user by email and password

    Args:
    - email (string)
    - password(string)

    Returns:
    - dict: the authentication status and the user ID if successful
    """
    users_collection = current_app.mongo.db.users
    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return {"status": 0, "id": str(user['_id'])}
        
    return {"status": 1, "id": None}

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
    except Exception as reg_error:
        return {"status": 1, "message": str(reg_error)}

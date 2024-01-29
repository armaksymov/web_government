"""
This module defines the main blueprint for the Flask application.
"""
from __future__ import annotations

import pyotp

from flask import session
from flask import jsonify
from flask import request
from flask import Blueprint
from base64 import b32encode
from flask import render_template

from app.services.information_service import *
from app.services.auth_service import register_user
from app.services.auth_service import delete_account
from app.services.auth_service import change_password
from app.services.auth_service import authenticate_user
from app.services.auth_service import get_b64encoded_qr_image

main_blueprint = Blueprint("main", __name__)


class Main:
    """
    The main routing blueprint.
    """

    ACCOUNT_ID = None

    @staticmethod
    @main_blueprint.route("/options", methods=["OPTIONS"])
    def my_options_route():
        """
        Handles the OPTIONS request for a specific route.

        This method provides information about the supported HTTP methods
        for a particular route and any additional headers that can be used.

        Returns:
        - Response object: Response with the allowed methods and headers.
        """

        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        allowed_headers = ["Content-Type", "Authorization"]

        response_headers = {
            "Allow": ", ".join(allowed_methods),
            "Access-Control-Allow-Methods": ", ".join(allowed_methods),
            "Access-Control-Allow-Headers": ", ".join(allowed_headers),
        }

        return (
            jsonify({"message": "OPTIONS request handled successfully"}),
            200,
            response_headers,
        )

    @staticmethod
    @main_blueprint.route("/")
    def landing_page():
        """
        Render the landing.html template.

        Returns:
        - render_template: HTML response with the content of landing.html.
        """

        return render_template("landing.html")

    @staticmethod
    @main_blueprint.route("/dashboard")
    def index_page():
        """
        Render the index.html template.
        Returns:
        - render_template: HTML response with the content of index.html.
        """

        return render_template("index.html")

    @staticmethod
    @main_blueprint.route("/feed")
    def feed_page():
        """
        Render the feed.html template.

        Returns:
        - render_template: HTML response with the content of feed.html.
        """

        # Fetch account information and display the user name
        user_id = session.get("account_id")
        if user_id:
            users_collection = current_app.mongo.db.users
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            name_value = user.get("first_name", "User")

        return render_template("feed.html", Name=name_value)

    @staticmethod
    @main_blueprint.route("/documents")
    def documents_page():
        """
        Render the documents.html template.

        Returns:
        - render_template: HTML response with the content of documents.html.
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        documents = get_documents(account_id)

        return render_template("documents.html", documents_data=documents)

    @staticmethod
    @main_blueprint.route("/services")
    def services_page():
        """
        Render the services.html template.

        Returns:
        - render_template: HTML response with the content of services.html.
        """

        return render_template("services.html")

    @staticmethod
    @main_blueprint.route("/profile")
    def profile_page():
        """
        Render the profile.html template.

        Returns:
        - render_template: HTML response with the content of profile.html.
        """

        return render_template("profile.html")

    @staticmethod
    @main_blueprint.route("/login")
    def login_page():
        """
        Render the login.html template.

        Returns:
        - render_template: HTML response with the content of login.html.
        """

        return render_template("login.html")

    @staticmethod
    @main_blueprint.route("/setup_2fa")
    def setup_2fa():
        """
        Sets up two-factor authentication (2FA) for the user.

        This method generates a Time-based One-Time Password (TOTP) and
        provides a QR code for the user to scan with their authenticator app.

        Returns:
        - Rendered template: HTML page for setting up 2FA with QR code.
        """

        session["account_id"] = request.args.get("id")
        id = b32encode(("wg" + session["account_id"]).encode()).decode("utf-8")

        totp_auth = pyotp.totp.TOTP(id).provisioning_uri(
            name=request.args.get("full_name"), issuer_name="web.gov"
        )

        qr_image = get_b64encoded_qr_image(totp_auth)

        return render_template("setup_2fa.html", qr=qr_image, account_id=id)
        return render_template("setup_2fa.html")

    @staticmethod
    @main_blueprint.route("/verify_2fa")
    def verify_2fa_page():
        """
        Renders the page for verifying two-factor authentication (2FA).

        If the account_id is provided in the request arguments, it sets
        the session's account_id to the provided value.

        Returns:
        - Rendered template: HTML page for verifying 2FA.
        """

        if request.args.get("id") != None:
            # account_id is already assigned
            session["account_id"] = request.args.get("id")

        return render_template("verify_2fa.html")

    @staticmethod
    @main_blueprint.route("/verify_2fa", methods=["POST"])
    def verify_2fa():
        """
        Verifies the two-factor authentication (2FA) code provided by the user.

        This method compares the provided OTP (One-Time Password) with the
        TOTP generated using the stored secret key.

        Returns:
        - JSON response: Status indicating the result of the verification.
        """

        secret_key = b32encode(("wg" + session["account_id"]).encode()).decode("utf-8")
        totp = pyotp.TOTP(secret_key)
        data = request.get_json()
        response = None

        if totp.verify(data["otp"]):
            response = {"status": 0}
        else:
            response = {"status": 1}

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/login", methods=["POST"])
    def authenticate():
        """
        Authenticate the user based on the provided JSON data.

        JSON Request:
        - email: User's email address.
        - password: User's password.

        Returns:
        - jsonify: JSON response indicating the status of the authentication.
          Format: {"status": int, "id": str}
        """

        data = request.get_json()
        response = authenticate_user(data["email"], data["password"])

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/register")
    def register_page():
        """
        Render the register.html template.

        Returns:
        - render_template: HTML response with the content of register.html.
        """

        return render_template("register.html")

    @staticmethod
    @main_blueprint.route("/register", methods=["POST"])
    def account_registration():
        """
        Create a new user account based on the provided JSON data.

        JSON Request:
        - first_name: User's first name.
        - last_name: User's last name.
        - email: User's email address.
        - password: User's password.

        Returns:
        - jsonify: JSON response indicating the status of the account creation.
          Format: {"status": int, "id": str}
        """

        data = request.get_json()
        response = register_user(
            data["first_name"],
            data["last_name"],
            data["email"],
            data["password"],
        )

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/license_and_registration")
    def license_and_registration_page():
        """
        Render the license_and_registration.html template.

        Returns:
        - render_template: HTML response with the content of license_and_registration.html.
        """

        license_and_registration = get_license_and_registration(Main.ACCOUNT_ID)
        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        license_and_registration = get_license_and_registration(account_id)

        return render_template(
            "license_and_registration.html",
            license_and_registration_data=license_and_registration,
        )

    @staticmethod
    @main_blueprint.route("/property_tax_payments")
    def property_tax_payments_page():
        """
        Render the property_tax_payments.html template.

        Returns:
        - render_template: HTML response with the content of property_tax_payments.html.
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        property_taxes = get_property_taxes(account_id)

        return render_template(
            "property_tax_payments.html",
            property_taxes_data=property_taxes,
        )

    @staticmethod
    @main_blueprint.route("/pay_property_tax", methods=["PUT"])
    def pay_property_tax():
        """
        Pay property tax based on the Account ID and provided JSON data.

        Account ID stored in session

        JSON Request:
        - Utility Bill Information

        Returns:
        - jsonify: JSON response indicating the status of the bill payment.
          Format: {"status": int, "id": str}
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        response = pay_property_tax(account_id)

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/utility_bill_payments")
    def utility_bill_payments_page():
        """
        Render the utility_bill_payments.html template.

        Returns:
        - render_template: HTML response with the content of utility_bill_payments.html.
        """
        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        utility_bills = get_utility_bills(account_id)

        return render_template("utility_bill_payments.html", bills_data=utility_bills)

    @staticmethod
    @main_blueprint.route("/pay_utility_bill", methods=["PUT"])
    def pay_utility_bill():
        """
        Pay unility bill based on the Account ID and provided JSON data.

        Account ID stored in session

        JSON Request:
        - Utility Bill Information

        Returns:
        - jsonify: JSON response indicating the status of the bill payment.
          Format: {"status": int, "id": str}
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        data = request.get_json()
        response = pay_utility_bill(account_id, data["bill"])

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/renew_license", methods=["POST"])
    def renew_license():
        """
        Renew the user's license.

        Returns:
        - Flask Response: JSON response with the status of the license renewal operation.
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        response = renew_license(account_id)

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/renew_registration", methods=["POST"])
    def renew_registration():
        """
        Renew the user's registration.

        Returns:
        - Flask Response: JSON response with the status of the registration renewal operation.
        """

        account_id = session.get("account_id")
        if account_id is None:
            return "Error: Account id is not set", 400

        response = renew_registration(account_id)

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/change_password")
    def change_password_page():
        """
        Render the change password page.

        Returns:
        - Flask Response: Rendered HTML template for the change password page.
        """

        return render_template("change_password.html")

    @staticmethod
    @main_blueprint.route("/change_password", methods=["PATCH"])
    def change_password():
        """
        Change the user's password.

        Returns:
        - Flask Response: JSON response with the status of the password change operation.
        """

        data = request.get_json()
        response = change_password(
            session.get("account_id"), data["old_pass"], data["new_pass"]
        )

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/delete_account")
    def delete_account_page():
        """
        Render the delete account page.

        Returns:
        - Flask Response: Rendered HTML template for the delete account page.
        """

        return render_template("delete_account.html")

    @staticmethod
    @main_blueprint.route("/delete_account", methods=["DELETE"])
    def delete_account():
        """
        Delete the user's account.

        Returns:
        - Flask Response: JSON response with the status of the account deletion operation.
        """

        response = delete_account(session.get("account_id"))

        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/my_profile")
    def my_profile_page():
        """
        Render the user's profile page.

        Returns:
        - Flask Response: Rendered HTML template for the user's profile page.
        """

        account_info = get_account_information(session.get("account_id"))
        return render_template("my_profile.html", account_data=account_info)

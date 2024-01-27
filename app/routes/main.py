"""
This module defines the main blueprint for the Flask application.
"""
from __future__ import annotations

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask import session

from app.services.auth_service import authenticate_user
from app.services.auth_service import register_user
from app.services.information_service import *

main_blueprint = Blueprint('main', __name__)


class Main:
    """
    The main routing blueprint.
    """

    ACCOUNT_ID = None

    @staticmethod
    @main_blueprint.route('/')
    def landing_page():
        """
        Render the landing.html template.

        Returns:
        - render_template: HTML response with the content of landing.html.
        """

        return render_template('landing.html')

    @staticmethod
    @main_blueprint.route('/dashboard')
    def index_page():
        """
        Render the index.html template.
        Returns:
        - render_template: HTML response with the content of index.html.
        """
        session['account_id'] = request.args.get('id')
        return render_template('index.html')

    @staticmethod
    @main_blueprint.route('/feed')
    def feed_page():
        """
        Render the feed.html template.

        Returns:
        - render_template: HTML response with the content of feed.html.
        """

        # # Fetch account information and display the user name
        # user_id = session.get("account_id")
        # if user_id:
        #     users_collection = current_app.mongo.db.users
        #     user = users_collection.find_one({"_id": ObjectId(user_id)})
        #     name_value = user.get("first_name", "User")

        # return render_template("feed.html", Name=name_value)
        return render_template('feed.html')

    @staticmethod
    @main_blueprint.route('/documents')
    def documents_page():
        """
        Render the documents.html template.

        Returns:
        - render_template: HTML response with the content of documents.html.
        """
        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400

        documents = get_documents(account_id)

        return render_template('documents.html', documents_data=documents)

    @staticmethod
    @main_blueprint.route('/services')
    def services_page():
        """
        Render the services.html template.

        Returns:
        - render_template: HTML response with the content of services.html.
        """

        return render_template('services.html')

    @staticmethod
    @main_blueprint.route('/profile')
    def profile_page():
        """
        Render the profile.html template.

        Returns:
        - render_template: HTML response with the content of profile.html.
        """

        return render_template('profile.html')

    @staticmethod
    @main_blueprint.route('/login')
    def login_page():
        """
        Render the login.html template.

        Returns:
        - render_template: HTML response with the content of login.html.
        """

        return render_template('login.html')

    @staticmethod
    @main_blueprint.route('/login', methods=['POST'])
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
        response = authenticate_user(data['email'], data['password'])

        return jsonify(response)

    @staticmethod
    @main_blueprint.route('/register')
    def register_page():
        """
        Render the register.html template.

        Returns:
        - render_template: HTML response with the content of register.html.
        """

        return render_template('register.html')

    @staticmethod
    @main_blueprint.route('/register', methods=['POST'])
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
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password'],
        )

        return jsonify(response)

    @staticmethod
    @main_blueprint.route('/license_and_registration')
    def license_and_registration_page():
        """
        Render the license_and_registration.html template.

        Returns:
        - render_template: HTML response with the content of license_and_registration.html.
        """

        license_and_registration = get_license_and_registration(Main.ACCOUNT_ID)
        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400

        license_and_registration = get_license_and_registration(account_id)

        return render_template(
            'license_and_registration.html',
            license_and_registration_data=license_and_registration,
        )

    @staticmethod
    @main_blueprint.route('/property_tax_payments')
    def property_tax_payments_page():
        """
        Render the property_tax_payments.html template.

        Returns:
        - render_template: HTML response with the content of property_tax_payments.html.
        """

        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400

        property_taxes = get_property_taxes(account_id)

        return render_template(
            'property_tax_payments.html', property_taxes_data=property_taxes,
        )

    @staticmethod
    @main_blueprint.route('/pay_property_tax', methods=['POST'])
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

        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400
        
        response = pay_property_tax(account_id)

        return jsonify(response)

    @staticmethod
    @main_blueprint.route('/utility_bill_payments')
    def utility_bill_payments_page():
        """
        Render the utility_bill_payments.html template.

        Returns:
        - render_template: HTML response with the content of utility_bill_payments.html.
        """
        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400

        utility_bills = get_utility_bills(account_id)

        return render_template('utility_bill_payments.html', bills_data=utility_bills)

    @staticmethod
    @main_blueprint.route('/pay_utility_bill', methods=['POST'])
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

        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400

        data = request.get_json()
        response = pay_utility_bill(account_id, data['bill'])

        return jsonify(response)

    @staticmethod
    @main_blueprint.route('/renew_license', methods=['POST'])
    def renew_license():

        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400
        
        response = renew_license(account_id)

        return jsonify(response)

    @staticmethod
    @main_blueprint.route('/renew_registration', methods=['POST'])
    def renew_registration():
        account_id = session.get('account_id')
        if account_id is None:
            return 'Error: Account id is not set', 400
        
        response = renew_registration(account_id)

        return jsonify(response)

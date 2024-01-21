"""
This module defines the main blueprint for the Flask application.
"""

from flask import current_app, Blueprint, request, render_template, jsonify
import bcrypt
from ..services.auth_service import authenticate_user, register_user
main_blueprint = Blueprint("main", __name__)


class Main:
    """
    The main routing blueprint.
    """

    ACCOUNT_ID = None

    @staticmethod
    @main_blueprint.route("/")
    def index():
        """
        Render the index.html template.

        Returns:
        - render_template: HTML response with the content of index.html.
        """

        Main.ACCOUNT_ID = request.args.get("id")

        return render_template("index.html")

    @staticmethod
    @main_blueprint.route("/feed")
    def feed():
        """
        Render the feed.html template.

        Returns:
        - render_template: HTML response with the content of feed.html.
        """

        return render_template("feed.html")

    @staticmethod
    @main_blueprint.route("/documents")
    def documents():
        """
        Render the documents.html template.

        Returns:
        - render_template: HTML response with the content of documents.html.
        """

        return render_template("documents.html")

    @staticmethod
    @main_blueprint.route("/services")
    def services():
        """
        Render the services.html template.

        Returns:
        - render_template: HTML response with the content of services.html.
        """

        return render_template("services.html")

    @staticmethod
    @main_blueprint.route("/profile")
    def profile():
        """
        Render the profile.html template.

        Returns:
        - render_template: HTML response with the content of profile.html.
        """

        return render_template("profile.html")

    @staticmethod
    @main_blueprint.route("/login")
    def login():
        """
        Render the login.html template.

        Returns:
        - render_template: HTML response with the content of login.html.
        """

        return render_template("login.html")

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
        response = authenticate_user(data['email'], data['password'])
        return jsonify(response)

    @staticmethod
    @main_blueprint.route("/register")
    def register():
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
        response = register_user(data['first_name'], data['last_name'],
                                  data['email'], data['password'])
        return jsonify(response)
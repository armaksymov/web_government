from flask import Blueprint, render_template, request, jsonify

services_blueprint = Blueprint("services", __name__)


@services_blueprint.route("/")
def index():
    """
    Render the index.html template.

    Returns:
    - render_template: HTML response with the content of index.html.
    """
    account_id = request.args.get("id")

    # TODO: Utilize the account id

    return render_template("index.html")


@services_blueprint.route("/feed")
def feed():
    """
    Render the feed.html template.

    Returns:
    - render_template: HTML response with the content of feed.html.
    """
    return render_template("feed.html")


@services_blueprint.route("/documents")
def documents():
    """
    Render the documents.html template.

    Returns:
    - render_template: HTML response with the content of documents.html.
    """
    return render_template("documents.html")


@services_blueprint.route("/services")
def services():
    """
    Render the services.html template.

    Returns:
    - render_template: HTML response with the content of services.html.
    """
    return render_template("services.html")


@services_blueprint.route("/profile")
def profile():
    """
    Render the profile.html template.

    Returns:
    - render_template: HTML response with the content of profile.html.
    """
    return render_template("profile.html")


@services_blueprint.route("/login")
def login():
    """
    Render the login.html template.

    Returns:
    - render_template: HTML response with the content of login.html.
    """
    return render_template("login.html")


@services_blueprint.route("/login", methods=["POST"])
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

    # TODO: Authenticate the account based on the received data

    # For demonstration purposes, let's assume authentication was successful
    status = 200
    account_id = "some_unique_id"  # TODO: Replace this with the actual account ID

    response_data = {"status": status, "id": account_id}

    return jsonify(response_data)


@services_blueprint.route("/register")
def register():
    """
    Render the register.html template.

    Returns:
    - render_template: HTML response with the content of register.html.
    """
    return render_template("register.html")


@services_blueprint.route("/register", methods=["POST"])
def account_registration():
    """
    Create a new user account based on the provided JSON data.

    JSON Request:
    - firstName: User's first name.
    - lastName: User's last name.
    - email: User's email address.
    - password: User's password.

    Returns:
    - jsonify: JSON response indicating the status of the account creation.
      Format: {"status": int, "id": str}
    """
    data = request.get_json()

    # TODO: Create the account based on the received data

    # For demonstration purposes, let's assume account creation was successful
    status = 200
    account_id = "some_unique_id"  # TODO: Replace this with the actual account ID

    response_data = {"status": status, "id": account_id}

    return jsonify(response_data)

from flask import Blueprint, render_template

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route("/")
def index():
    """
    Render the index.html template.

    Returns:
    - render_template: HTML response with the content of index.html.
    """
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
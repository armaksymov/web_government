from flask import Blueprint, render_template

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route("/services")
def index():
    return render_template("services.html")

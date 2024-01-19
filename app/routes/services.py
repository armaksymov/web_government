""" A module for the services page """

from flask import Blueprint, render_template

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route("/services")
def index():
    """ Endpoint for the /services route """
    return render_template("services.html")

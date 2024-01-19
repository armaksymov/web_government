""" A module for the index page """

from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    """ Endpoint for the / route """
    return render_template("index.html")

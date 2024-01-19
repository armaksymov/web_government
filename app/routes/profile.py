""" A module for the profile page """

from flask import Blueprint, render_template

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route("/profile")
def index():
    """ Endpoint for the /profile route """
    return render_template("profile.html")

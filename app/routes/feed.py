""" A module for the feed page """

from flask import Blueprint, render_template

feed_blueprint = Blueprint('feed', __name__)

@feed_blueprint.route("/feed")
def index():
    """ Endpoint for the /feed route """
    return render_template("feed.html")

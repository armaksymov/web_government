from flask import Blueprint, render_template

feed_blueprint = Blueprint('feed', __name__)

@feed_blueprint.route("/feed")
def index():
    return render_template("feed.html")

from flask import Blueprint, render_template

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route("/profile")
def index():
    return render_template("profile.html")

from flask import Blueprint, render_template

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route("/register")
def index():
    return render_template("register.html")

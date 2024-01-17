from flask import Blueprint, render_template

documents_blueprint = Blueprint('documents', __name__)

@documents_blueprint.route("/documents")
def index():
    return render_template("documents.html")

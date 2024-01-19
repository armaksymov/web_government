""" A module for the documents page """

from flask import Blueprint, render_template

documents_blueprint = Blueprint('documents', __name__)

@documents_blueprint.route("/documents")
def index():
    """ Endpoint for the /documents route """
    return render_template("documents.html")

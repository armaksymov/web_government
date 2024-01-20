"""
This script defines a Flask application incorporating a modular structure using blueprints.
It creates an instance of the Flask class, registers a blueprint for services, and provides
a convenient way to run the application.

Attributes:
    app (Flask): The main Flask application instance.

Usage:
    Run this script to start the Flask application.
    By default, the application will be accessible at http://127.0.0.1:5000/ in debug mode.

Example:
    $ python run.py

Note:
    Ensure that the necessary dependencies are installed before running the application.
"""

from flask import Flask
from app.routes.services import services_blueprint

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.register_blueprint(services_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
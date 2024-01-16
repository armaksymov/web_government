from flask import Flask
from app.routes.main import main_blueprint

app = Flask(__name__, template_folder='app/templates')
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

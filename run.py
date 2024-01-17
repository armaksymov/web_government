from flask import Flask
from app.routes.main import main_blueprint
from app.routes.feed import feed_blueprint
from app.routes.profile import profile_blueprint
from app.routes.services import services_blueprint
from app.routes.documents import documents_blueprint

app = Flask(__name__, template_folder='app/templates')

app.register_blueprint(main_blueprint)
app.register_blueprint(feed_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(services_blueprint)
app.register_blueprint(documents_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

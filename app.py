from dotenv import load_dotenv
import os
from flask import Flask
from flask_talisman import Talisman
from views import bp
from database import client


load_dotenv()


def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp)

    Talisman(app)

    # Secret Key config for WTF forms.
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    # Session config. Followed documentation
    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB"] = client
    app.config["SESSION_MONGODB_DB"] = "standups"
    app.config["SESSION_MONGODB_COLLECT"] = "sessions"

    return app

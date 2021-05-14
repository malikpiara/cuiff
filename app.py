from dotenv import load_dotenv
import os
from flask import Flask
from flask_talisman import Talisman
from views import bp
from database import client
from flask_mail import Mail


load_dotenv()


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

""" app.config["FUZZBOARD_ADMIN"] = os.environ.get("FUZZBOARD_ADMIN")

# Email setup
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app) """

if __name__ == '__main__':
    app.run()

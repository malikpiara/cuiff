from dotenv import load_dotenv
import os
from flask import Flask
from flask_talisman import Talisman
from .views import bp
from .auth import auth
from .database import client
from .emails import mail

load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp)
app.register_blueprint(auth)

csp = {
    'default-src': [
        '\'self\'',
        '*.googleapis.com',
        '*.gstatic.com',
        'cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css',
    ],
    'img-src': '*',
}
Talisman(app, content_security_policy=csp)

# Secret Key config for WTF forms.
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Session config. Followed documentation
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = client
app.config["SESSION_MONGODB_DB"] = "standups"
app.config["SESSION_MONGODB_COLLECT"] = "sessions"

app.config["FUZZBOARD_ADMIN"] = os.environ.get("FUZZBOARD_ADMIN")

# Email setup
app.config["MAIL_SERVER"] = 'smtp.sendgrid.net'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER')


mail.init_app(app)

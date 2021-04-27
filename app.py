from dotenv import load_dotenv
import os
from forms import Entry, SignIn, SignUp, UserSettings
import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_talisman import Talisman
from views import test

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(test)
    Talisman(app)

    # Secret Key config for WTF forms.
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    # MongoDB Setup
    client = MongoClient(os.environ.get("MONGODB_URI"),
                         ssl=True, ssl_cert_reqs='CERT_NONE')
    app.db = client.standups

    # Session config. Followed documentation
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB"] = client
    app.config["SESSION_MONGODB_DB"] = "standups"
    app.config["SESSION_MONGODB_COLLECT"] = "sessions"

    Session(app)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = SignIn()
        # If username is already stored in the session
        # redirect user to the homepage.
        if session.get("username"):
            return redirect(url_for("home"))
        # Se o nome submitido tiver na base de dados
        # Store in session e redirect para a homepage.
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data
            db_name = app.db.users.find_one(
                {
                    "name": name
                }
            )

            if db_name:
                check = check_password_hash(db_name["password"], password)

                if check:
                    session["username"] = name
                    return redirect(url_for("home"))
            else:
                print("Somethings wrong")
        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout():
        session["username"] = None
        return redirect("/login")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        form = SignUp()
        if session.get("username"):
            return redirect(url_for("home"))
        if form.validate_on_submit():
            email_address = form.email_address.data
            name = form.name.data
            hashed_pass = generate_password_hash(
                form.password.data)
            app.db.users.insert(
                {
                    "email": email_address,
                    "name": name,
                    "password": hashed_pass
                }
            )
            return redirect(url_for("home"))
        return render_template("signup.html", form=form)

    def get_entries():
        entries = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d %H-%M-%S").strftime("%b %d, %Y"),
                entry["author"]
            )
            for entry in app.db.entries.find({}).sort([("date", -1)])
        ]
        return entries

    @app.route("/", methods=["GET", "POST"])
    def home():
        form = Entry()
        if not session.get("username"):
            return redirect("/login")
        if form.validate_on_submit():
            entry_content = form.entry_input.data
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
            app.db.entries.insert(
                {
                    "content": entry_content,
                    "date": formatted_date,
                    "author": session["username"]
                }
            )
            return redirect(url_for('home'))

        # Showing entries from database on the page.
        entries = get_entries()

        return render_template("home.html", entries=entries, form=form)

    @app.route("/settings")
    def settings():
        form = UserSettings()
        name = session["username"]
        user_information = app.db.users.find_one(
            {
                "name": name
            }
        )

        return render_template("settings.html",
                               user_information=user_information, form=form)

    return app

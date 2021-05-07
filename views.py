from flask import Flask, Blueprint, render_template, redirect, url_for, session
from flask_session import Session
import datetime
import os
from pymongo import MongoClient
from forms import Entry, SignIn, SignUp, UserSettings
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

app = Flask(__name__)

Session(app)


# MongoDB Setup
client = MongoClient(os.environ.get("MONGODB_URI"),
                     ssl=True, ssl_cert_reqs='CERT_NONE')
app.db = client.standups


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


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = SignIn()
    # If username is already stored in the session
    # redirect user to the homepage.
    if session.get("username"):
        return redirect(url_for('main.home'))
    # Se o nome submitido tiver na base de dados
    # Store in session e redirect para a homepage.
    if form.validate_on_submit():
        email = form.email_address.data
        password = form.password.data
        db_email = app.db.users.find_one(
            {
                "email": email
            }
        )

        if db_email:
            check = check_password_hash(db_email["password"], password)

            if check:
                session["username"] = email
                return redirect(url_for('main.home'))
        else:
            print("Somethings wrong")
    return render_template("login.html", form=form)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUp()
    if session.get("username"):
        return redirect(url_for('main.home'))
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
        return redirect(url_for('main.home'))
    return render_template("signup.html", form=form)


@bp.route("/", methods=["GET", "POST"])
def home():
    if not session.get("username"):
        return redirect("/login")
    form = Entry()
    email = session["username"]
    user_information = app.db.users.find_one(
        {
            "email": email
        }
    )
    if form.validate_on_submit():
        entry_content = form.entry_input.data
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
        app.db.entries.insert(
            {
                "content": entry_content,
                "date": formatted_date,
                "author": user_information["name"]
            }
        )
        return redirect(url_for('main.home'))

    # Showing entries from database on the page.
    entries = get_entries()

    return render_template("home.html", entries=entries, form=form, user_information=user_information)


@bp.route("/settings")
def settings():
    form = UserSettings()
    email = session["username"]
    user_information = app.db.users.find_one(
        {
            "email": email
        }
    )

    return render_template("settings.html",
                           user_information=user_information, form=form)


@bp.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login")


@bp.route("/progress/<author>")
def progress(author):
    entries = get_entries()

    return render_template("progress.html", entries=entries, author=author)

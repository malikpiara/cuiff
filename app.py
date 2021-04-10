from dotenv import load_dotenv
import os
from forms import Entry, SignIn, SignUp
import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Secret Key config for WTF forms.
    # There's a better way of doing this.
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    # MongoDB Setup
    client = MongoClient(os.environ.get("MONGODB_URI"),
                         ssl=True, ssl_cert_reqs='CERT_NONE')
    app.db = client.standups

    # Session config. Followed documentation
    # Will have to change this and connect with MongoDB to deploy
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    # app.config["SESSION_MONGODB"] = client
    # app.config["SESSION_MONGODB_DB"] = client.standups

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
                print(name)
                print(password)
                print(check)
                if check_password_hash(db_name["password"], password):
                    print(name)
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

    @app.route("/", methods=["GET", "POST"])
    def home():
        form = Entry()
        if not session.get("username"):
            return redirect("/login")
        if form.validate_on_submit():
            entry_content = form.entry_input.data
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert(
                {
                    "content": entry_content,
                    "date": formatted_date,
                    "author": session["username"]
                }
            )
            return redirect(url_for('home'))

        # Showing entries from database on the page.
        entries = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
                entry["author"]
            )
            for entry in app.db.entries.find({}).sort([("date", -1)])
        ]

        return render_template("home.html", entries=entries, form=form)

    @app.route("/progress/<author>")
    def progress(author):
        entries = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
                entry["author"]
            )
            for entry in app.db.entries.find({}).sort([("date", -1)])
        ]

        return render_template("progress.html", entries=entries, author=author)

    if __name__ == '__main__':
        app.run(debug=True)
    return app

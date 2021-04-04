import os
import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Session config. Followed documentation
    # Will have to change this and connect with MongoDB to deploy
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    client = MongoClient(os.environ.get("MONGODB_URI"),
                         ssl=True, ssl_cert_reqs='CERT_NONE')
    app.db = client.standups

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            session["username"] = request.form.get("username")
            return redirect("/")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session["username"] = None
        return redirect("/login")

    @app.route("/", methods=["GET", "POST"])
    def home():
        if not session.get("username"):
            return redirect("/login")
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert(
                {"content": entry_content, "date": formatted_date, "author": session["username"]})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
                entry["author"]
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    @app.route("/progress/<author>")
    def progress(author):
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
                entry["author"]
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("progress.html",
                               entries=entries_with_date, author=author)

    return app

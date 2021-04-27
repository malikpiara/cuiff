from flask import Flask, Blueprint, render_template
import datetime
import os
from pymongo import MongoClient

test = Blueprint('test', __name__)

app = Flask(__name__)

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


@test.route("/progress/<author>")
def progress(author):
    entries = get_entries()

    return render_template("progress.html", entries=entries, author=author)

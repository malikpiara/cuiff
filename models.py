import datetime
from werkzeug.security import generate_password_hash
from database import client
from flask import current_app


def get_entries():
    entries = [
        {
            "content": entry["content"],
            "date": entry["date"],
            "formatted_date": datetime.datetime.strptime(
                entry["date"], "%Y-%m-%d %H-%M-%S").strftime("%b %d, %Y"),
            "user_id": entry["user_id"],
            "user_name": client.standups.users.find_one({"_id": entry["user_id"]})["name"]
        }
        for entry in client.standups.entries.find(
            {
                "user_id": {"$exists": True}
            }
        ).sort([("date", -1)])
    ]
    return entries


def find_user_by_email(email):
    return client.standups.users.find_one(
        {
            "email": email
        }
    )


def create_user(email_address, name, password):
    hashed_pass = generate_password_hash(
        password)
    client.standups.users.insert(
        {
            "email": email_address,
            "name": name,
            "password": hashed_pass
        }
    )
    """ send_email(current_app.config["FUZZBOARD_ADMIN"],
               "New User", "New User signed up") """


def update_user(email_address, name, new_email):
    client.standups.users.update_one(
        {
            'email': email_address
        },
        {
            "$set": {'name': name, 'email': new_email}
        }
    )


def delete_user(user_id, email_address):
    client.standups.entries.delete_many(
        {
            'user_id': user_id
        }
    )
    client.standups.users.delete_one(
        {
            'email': email_address
        }
    )


def create_entry(content, user_id):
    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
    client.standups.entries.insert(
        {
            "content": content,
            "date": formatted_date,
            "user_id": user_id
        }
    )

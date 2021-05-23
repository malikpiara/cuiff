import datetime
from werkzeug.security import generate_password_hash
from .database import client
from werkzeug.security import check_password_hash
from flask import flash


def get_entries():
    # Assign client.standups.users.find_one({"_id": entry["user_id"]})["name"]
    # to a variable.
    entries = [
        {
            "board_id": entry["board_id"],
            "content": entry["content"],
            "date": entry["date"],
            "formatted_date": datetime.datetime.strptime(
                entry["date"], "%Y-%m-%d %H-%M-%S").strftime("%b %d, %Y"),
            "user_id": entry["user_id"],
            "user_name": client.standups.users.find_one({"_id": entry["user_id"]})["name"],
            "first_name_initial": client.standups.users.find_one({"_id": entry["user_id"]})["name"][0],
            "second_name_initial": client.standups.users.find_one({"_id": entry["user_id"]})["name"].split()[1][0] if len(client.standups.users.find_one({"_id": entry["user_id"]})["name"].split()) > 1 else ""
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


def create_board(owner, question, visibility):
    # Build a view function and try create new boards
    # without real data first
    client.standups.boards.insert(
        {
            "owner": owner,
            "question": question,
            "visibility": visibility,
            "id": "3"
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


def update_name(email_address, name):
    client.standups.users.update_one(
        {
            'email': email_address
        },
        {
            "$set": {'name': name}
        }
    )


def update_email(email_address, new_email):
    client.standups.users.update_one(
        {
            'email': email_address
        },
        {
            "$set": {'email': new_email}
        }
    )


def update_password(email_address, old_password, new_password):
    hashed_pass = generate_password_hash(
        new_password)

    user = find_user_by_email(email_address)
    check_password = check_password_hash(user["password"], old_password)

    if check_password:
        client.standups.users.update_one(
            {
                'email': email_address
            },
            {
                "$set": {'password': hashed_pass}
            }
        )


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


def create_entry(content, user_id, board_id):
    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
    client.standups.entries.insert(
        {
            "content": content,
            "date": formatted_date,
            "user_id": user_id,
            "board_id": board_id
        }
    )


def get_board(board_id):
    boards = [
        {
            "board_id": board["id"],
            "question": board["question"],
            "owner": board["owner"]
        }
        for board in client.standups.boards.find(
            {
                "id": board_id
            }
        )
    ]
    return boards


def get_boards():
    boards = [
        {
            "question": board["question"],
            "owner": board["owner"]
        }
        for board in client.standups.boards.find(
            {
                "owner": {"$exists": True}
            }
        )
    ]
    return boards

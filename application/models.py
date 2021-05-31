import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from .database import client
from werkzeug.security import check_password_hash
from flask import flash
from bson.objectid import ObjectId


def get_entries(board_id):
    entries = []
    for entry in client.standups.entries.find(
        {
            "board_id": board_id
        }
    ):
        getName = client.standups.users.find_one(
            {"_id": entry["user_id"]})["name"]

        post = {"_id": entry["_id"],
                "board_id": entry["board_id"],
                "content": entry["content"],
                "date": entry["date"],
                "formatted_date": datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d %H-%M-%S").strftime("%b %d, %Y"),
                "user_id": entry["user_id"],
                "user_name": getName,
                "first_name_initial": getName[0],
                "second_name_initial": getName.split()[1][0] if len(getName.split()) > 1 else ""}

        entries.append(post)
    return sorted(entries, key=lambda post: post["date"], reverse=True)


def find_user_by_email(email):
    return client.standups.users.find_one(
        {
            "email": email
        }
    )


def find_space_by_owner_id(owner_id, type):
    return client.standups.spaces.find_one(
        {
            "owner_id": owner_id,
            "type": type
        }
    )


def get_board(board_id):

    boards = [
        {
            "_id": board["_id"],
            "question": board["question"],
            "owner_id": board["owner_id"]
        }
        for board in client.standups.boards.find(
            {
                "_id": ObjectId(board_id)
            }
        )
    ]
    return boards


def get_boards():
    boards = [
        {
            "_id": board["_id"],
            "question": board["question"],
            "owner_id": board["owner_id"],
            "visibility": board["visibility"]
        }
        for board in client.standups.boards.find(
            {
                "owner_id": {"$exists": True}
            }
        )
    ]
    return boards


def create_board(owner_id, question, visibility, space_id):
    client.standups.boards.insert(
        {
            "owner_id": owner_id,
            "question": question,
            "visibility": visibility,
            "space_id": space_id,
        }
    )


def create_space(owner_id, type):
    client.standups.spaces.insert(
        {
            "name": "Personal Boards",
            "members": owner_id,
            "owner_id": owner_id,
            "type": type
        }
    )


def create_user(email_address, name, password):
    hashed_pass = generate_password_hash(
        password)
    new_user = client.standups.users.insert(
        {
            "email": email_address,
            "name": name,
            "password": hashed_pass
        }
    )

    create_space(new_user, "personal")


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
            "board_id": ObjectId(board_id)
        }
    )


def get_entry(_id):
    entry = client.standups.entries.find_one(
        {
            "_id": _id
        }
    )
    return entry


def delete_entry(_id):
    # You should only be able to delete if your id is the author id
    client.standups.entries.delete_one(
        {
            "_id": ObjectId(_id)
        }
    )

import datetime
from werkzeug.security import generate_password_hash
from .database import client
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
import jwt
import os
from time import time


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
    return client.standups.users.find_one({"email": email})


def find_space_by_owner_id(owner_id, type):
    return client.standups.spaces.find_one(
        {
            "owner_id": owner_id,
            "type": type
        }
    )


def get_space_by_member_id(member_id):
    spaces = []
    for space in client.standups.spaces.find(
        {
            "members": member_id
        }
    ):
        workspace = {
            "_id": space["_id"],
            "name": space["name"],
            "members": space["members"],
            "owner_id": space["owner_id"],
            "type": space["type"]
        }
        spaces.append(workspace)
    return spaces


def get_spaces(user_id):
    spaces = []
    for space in client.standups.spaces.find(
        {
            "owner_id": user_id
        }
    ):
        workspace = {
            "_id": space["_id"],
            "name": space["name"],
            "members": space["members"],
            "owner_id": space["owner_id"],
            "type": space["type"]
        }
        spaces.append(workspace)
    return spaces


def get_board(board_id):
    return client.standups.boards.find_one({'_id': ObjectId(board_id)})


def get_space(space_id):
    return client.standups.spaces.find_one({'_id': ObjectId(space_id)})


def get_boards():
    boards = [
        {
            "_id": board["_id"],
            "question": board["question"],
            "owner_id": board["owner_id"],
            "visibility": board["visibility"],
            "space_id": board["space_id"]
        }
        for board in client.standups.boards.find(
            {
                "owner_id": {"$exists": True}
            }
        )
    ]
    return boards


def create_board(owner_id, question, space_id):
    client.standups.boards.insert_one(
        {
            "owner_id": owner_id,
            "question": question,
            "visibility": "private",
            "space_id": space_id,
        }
    )


def create_space(name, owner_id, type):
    client.standups.spaces.insert_one(
        {
            "name": name,
            "members": [owner_id],
            "owner_id": owner_id,
            "type": type
        }
    )


def create_user(email_address, name, password):
    # The active workspace should be the personal space that is created for the user.
    hashed_pass = generate_password_hash(
        password)
    new_user = {
        "email": email_address,
        "name": name,
        "password": hashed_pass,
        "active_workspace": ""
    }
    client.standups.users.insert_one(new_user)

    create_space("Personal Boards", new_user['_id'], "personal")


def check_invites(email_address):
    invites = []
    for invite in client.standups.user_invites.find(
        {
            "invite_recipient": email_address
        }
    ):
        space_invites = {
            "space": invite["space_id"],
            "invite_recipient": invite["invite_recipient"]
        }
        invites.append(space_invites)
    return invites


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


def update_active_workspace(id, workspace):
    return client.standups.users.find_one_and_update(
        {
            '_id': ObjectId(id)
        },
        {
            '$set': {'active_workspace': workspace}
        }
    )


def delete_user(user_id, email_address):
    # Deleting all of the entries posted by the user.
    # Then, deleting the user from the DB.
    client.standups.entries.delete_many({'user_id': user_id})
    client.standups.users.delete_one({'email': email_address})


def create_entry(_id, content, user_id, board_id):
    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
    client.standups.entries.insert_one(
        {
            "_id": _id,
            "content": content,
            "date": formatted_date,
            "user_id": user_id,
            "board_id": ObjectId(board_id)
        }
    )


def get_user(_id):
    return client.standups.users.find_one({"_id": ObjectId(_id)})


def get_entry(_id):
    return client.standups.entries.find_one({"_id": _id})


def create_invite_to_space(space_id, sender_id, recipient_email):
    client.standups.user_invites.insert_one(
        {
            "space_id": space_id,
            "invite_sender": sender_id,
            "invite_recipient": recipient_email,
        }
    )


def get_reset_password_token(user_id, expires_in=3600):
    # BUG: When the password is reset, the token apparently still works.
    return jwt.encode(
        {'reset_password':
            user_id, 'exp': time() + expires_in},
        os.environ.get('SECRET_KEY'), algorithm='HS256')


def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, os.environ.get('SECRET_KEY'),
                        algorithms=['HS256'])['reset_password']
    except:
        return
    return client.standups.users.find_one({'_id': ObjectId(id)})


def set_password(id, password):
    password_hash = generate_password_hash(password)

    return client.standups.users.find_one_and_update(
        {
            '_id': ObjectId(id)
        },
        {
            '$set': {'password': password_hash}
        }
    )


class DB_Update():
    # Temporary Functions used to update my models
    def add_active_workspace_to_user():
        for user in client.standups.users.find({'active_workspace': {"$exists": False}}):

            client.standups.users.update_one(
                {
                    '_id': user["_id"]
                },

                {
                    '$set':
                        {
                            'active_workspace': ''
                        }
                }
            )

# Aggregation


db = client["standups"]
user_collection = db["users"]
workspace_collection = db["spaces"]


def aggregation_test(workspace_id):
    pipeline = [
        {
            '$match': {
                '_id': ObjectId(workspace_id)
            }
        }
    ]
    results = workspace_collection.aggregate(pipeline)

    for entry in results:
        return entry['name']


# START OF LEMON ZEST
# Should I add updated_at, modified_by and created_at to my DB?
# TODO: Write methods to check if user can edit.
# TODO: Call methods that check if user can edit.
# TODO: Update check methods to include workspace admins so they can also edit?

def can_user_delete_entry(user_id, entry_id):
    entry = get_entry(entry_id)

    if entry["user_id"] == ObjectId(user_id):
        return True
    else:
        return False


def can_user_delete_board(user_id, board_id):
    board = get_board(board_id)

    if board["owner_id"] == ObjectId(user_id):
        return True
    else:
        return False


def can_user_delete_workspace(user_id, workspace_id):
    workspace = get_space(workspace_id)

    if workspace["owner_id"] == ObjectId(user_id):
        return True
    else:
        return False


def delete_entry(entry_id, user_id):
    if not can_user_delete_entry(user_id, entry_id):
        return

    client.standups.entries.update_one(
        {
            "_id": ObjectId(entry_id)
        },
        {
            "$set": {'deleted_at': datetime.datetime.today()}
        }
    )


def delete_all_entries_in_board(board_id):
    client.standups.entries.update_many(
        {
            'board_id': ObjectId(board_id)
        },
        {
            "$set": {'deleted_at': datetime.datetime.today()}
        }
    )


def delete_board(board_id, user_id):
    if not can_user_delete_board(user_id, board_id):
        return

    delete_all_entries_in_board(board_id)

    client.standups.boards.update_one(
        {
            '_id': ObjectId(board_id)
        },
        {
            "$set": {'deleted_at': datetime.datetime.today()}
        }
    )


def delete_all_boards_in_workspace(workspace_id):
    client.standups.boards.update_many(
        {
            'space_id': ObjectId(workspace_id)
        },
        {
            "$set": {'deleted_at': datetime.datetime.today()}
        }
    )


def delete_workspace(workspace_id, user_id):
    if not can_user_delete_workspace(user_id, workspace_id):
        return

    delete_all_boards_in_workspace(workspace_id)

    client.standups.spaces.update_one(
        {
            '_id': ObjectId(workspace_id)
        },
        {
            "$set": {'deleted_at': datetime.datetime.today()}
        }
    )


def rename_board(_id, new_question):
    # TODO: Write a wrapper function to check if user can rename the board.

    client.standups.boards.update_one(
        {
            '_id': ObjectId(_id)
        },
        {
            '$set': {'question': new_question}
        }
    )


def rename_workspace(_id, new_name):
    # TODO: Write a wrapper function to check if user can rename the workspace.

    client.standups.spaces.update_one(
        {
            '_id': ObjectId(_id)
        },
        {
            '$set': {'name': new_name}
        }
    )


def edit_entry(id, new_content):
    # TODO: Write a wrapper function to check if user can edit the entry.
    # Should I be storing a timestamp of when the entry was edited?
    client.standups.entries.update_one(
        {
            '_id': ObjectId(id)
        },
        {
            '$set': {'content': new_content}
        }
    )

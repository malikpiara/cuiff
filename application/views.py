from bson.errors import BSONError
from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask.globals import request
from .forms import ChangePasswordReal, Entry, SignIn, SignUp, UserSettings, DeleteUser, ChangeName, ChangeEmail, ChangePassword, ChangePasswordReal, NewBoard, NewSpace, InviteToSpace
from werkzeug.security import check_password_hash
from .models import create_board, create_space, delete_entry, get_boards, get_entries, find_user_by_email, create_user, create_entry, get_entry, update_user, delete_user, update_email, update_name, update_password, get_board, find_space_by_owner_id, get_spaces, get_space_by_member_id, create_invite_to_space, check_invites, get_user
from .emails import send_email
from bson.objectid import ObjectId
import datetime

bp = Blueprint('main', __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = SignIn()
    # If username is already stored in the session
    # redirect user to the homepage.
    if session.get("username"):
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        email = form.email_address.data
        password = form.password.data
        user = find_user_by_email(email)

        if user:
            check = check_password_hash(user["password"], password)
            # If user is found, store the email and id in session.
            if check:
                session["username"] = email
                session["user_id"] = str(user["_id"])
                return redirect(url_for('main.home'))

    return render_template("login.html", form=form)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUp()
    if session.get("username"):
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user_email = form.email_address.data
        user_name = form.name.data
        create_user(user_email,
                    user_name, password=form.password.data)

        #######################

        # I want to check if the email inserted is in the invites collection.
        # If the email is there, I want to add the user to the spaces with the space_id
        # in the database.

        # Add the new user to all the spaces that are returned (space_id)

        invites = check_invites(user_email)

        list_of_space_invites = []

        for s in range(len(invites)):
            if invites[s]["invite_recipient"]:
                list_of_space_invites.append(
                    (
                        invites[s]["space"]
                    )
                )

        print(list_of_space_invites)

        #######################

        send_email("Fuzzboard | New signup", "malikpiara@gmail.com",
                   "mail/email", user_email, user_name)
        send_email("Welcome to Fuzzboard", user_email,
                   "mail/new_signup", user_email, user_name)
        return redirect(url_for('main.home'))
    return render_template("signup.html", form=form)


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = UserSettings()
    change_name = ChangeName()
    change_email = ChangeEmail()
    change_password = ChangePassword()
    change_password_real = ChangePasswordReal()
    delete_user_button = DeleteUser()

    email = session["username"]
    user_information = find_user_by_email(email)

    # New name field
    if change_name.validate_on_submit():
        update_name(email_address=email,
                    name=change_name.name.data)
        flash("Your name was changed successfully.")

        return redirect(url_for('main.settings'))

    # New email field
    if change_email.validate_on_submit():
        new_email = change_email.email_address.data

        update_email(email_address=email,
                     new_email=new_email)
        flash("Your email was changed successfully.")

        session["username"] = new_email

        return redirect(url_for('main.settings'))

    # Change password old, new field
    if change_password_real.validate_on_submit():
        old_password = change_password_real.old_password.data
        new_password = change_password_real.new_password.data

        update_password(email_address=email,
                        old_password=old_password, new_password=new_password)
        flash("Your password was changed successfully.")

        return redirect(url_for('main.settings'))

    if delete_user_button.validate_on_submit():
        delete_user(user_id=user_information["_id"], email_address=email)
        session["username"] = None

        return redirect(url_for('main.login'))

    return render_template("settings.html",
                           user_information=user_information, form=form,
                           delete_user_button=delete_user_button, email=email,
                           change_name=change_name, change_email=change_email,
                           change_password=change_password,
                           change_password_real=change_password_real)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@bp.route("/", methods=["GET", "POST"])
def home():
    if not session.get("user_id"):
        return redirect("/login")

    user_id = ObjectId(session["user_id"])
    boards = get_boards()

    # TODO: Replace space_ function with spaces.
    #space_ = find_space_by_owner_id(user_id, "personal")
    spaces = get_space_by_member_id(user_id)

    new_list = []

    for s in range(len(spaces)):
        if spaces[s]["name"]:
            new_list.append(
                (
                    spaces[s]["_id"],
                    spaces[s]["name"]
                )
            )

    form = NewBoard()
    new_space_form = NewSpace()

    form.space.choices = new_list

    if form.validate_on_submit():
        create_board(user_id,
                     form.question.data,
                     ObjectId(form.space.data))
        return redirect("/")

    if new_space_form.validate_on_submit():
        create_space(new_space_form.name.data,
                     user_id,
                     "team",)
        return redirect("/")

    return render_template("page.html", user_id=user_id,
                           boards=boards, spaces=spaces,
                           form=form, new_space_form=new_space_form)


@bp.route("/invite", methods=["GET", "POST"])
# We cannot append the email address in the form to a database because we're using ids.
# Instead, we have to do something like storing the email address in an invites collection,
# sending an email notification and checking if the email address used is in the collection
# when a new user signs up to Fuzzboard.
def invitePeople():
    form = InviteToSpace()
    user_id = ObjectId(session["user_id"])
    if form.validate_on_submit():
        # TODO: Replace space_id placeholder with given space.
        create_invite_to_space(space_id=ObjectId("60b65e2ac456b5b074598a43"),
                               sender_id=user_id,
                               recipient_email=form.email.data)
        send_email(subject="Invite to join Fuzzboard",
                   to=form.email.data,
                   template="mail/invite_to_space",
                   user_email="",
                   user_name=""
                   )
    return render_template("invite.html", form=form)


@bp.route("/entries/<entry_id>", methods=["DELETE", "POST"])
def deleteEntry(entry_id):
    user_id = ObjectId(session["user_id"])
    entry = get_entry(ObjectId(entry_id))

    if entry["user_id"] == user_id:
        delete_entry(entry_id)

    else:
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))


@bp.route("/boards/<board_number>", methods=["GET"])
def board(board_number):
    try:
        # NOTE: converting board_number from string to ObjectId
        board_number = ObjectId(board_number)
    except BSONError:
        return redirect("/")
    form = Entry()
    user_id = ObjectId(session["user_id"])

    # Showing entries from database on the page.
    entries = get_entries(board_number)
    try:
        boards = get_board(board_number)
        # TODO: check if board is empty
    except BSONError:
        return redirect("/")

    return render_template("board.html", entries=entries,
                           board_number=board_number, form=form,
                           boards=boards, user_id=user_id)


@bp.route("/boards/<board_number>/<author>")
def progress(author, board_number):
    try:
        # NOTE: converting board_number from string to ObjectId
        board_number = ObjectId(board_number)
    except BSONError:
        return redirect("/")

    # Showing entries from database on the page.
    entries = get_entries(board_number)
    try:
        boards = get_board(board_number)
        # TODO: check if board is empty
    except BSONError:
        return redirect("/")

    return render_template("progress.html", entries=entries, author=author,
                           board_number=board_number,
                           boards=boards)


@bp.route("/boards/<board_number>", methods=["POST"])
def name_create(board_number):

    form = Entry()
    user_id = ObjectId(session["user_id"])
    board_number = ObjectId(board_number)

    formatted_date = datetime.datetime.today().strftime("%b %d, %Y")

    get_board(board_number)

    var = ObjectId()

    create_entry(_id=var, content=form.entry_input.data,
                 user_id=user_id, board_id=board_number)

    print(var)

    print(get_entry(var))

    post_info = get_entry(var)["content"]

    real_user_id = get_entry(var)["user_id"]
    print(post_info)

    print(get_user(real_user_id)["name"])

    user_name = get_user(real_user_id)["name"]
    first_name_initial = user_name[0]
    second_name_initial = user_name.split()[1][0] if len(
        user_name.split()) > 1 else ""

    response = f"""
    <article class="entry">
    <header>
                        <div class="profile-picture">
                            <a href="#">
                                <div class="profile-picture-initials">
                                { first_name_initial.capitalize() }{ second_name_initial.capitalize() }
                                </div>
                            </a>
                        </div>

                        
                        

                        <time class="entry_date" datetime="{{ entry.date }}">{ formatted_date }</time>
                        
                        <p class="entry_author">{ user_name }</p>
                    </header>
        
        
        {post_info}
    </article>
    """
    return response


@bp.route("/menu")
def menu():
    response = f"""
    <h1>This will be a fancy search.</h1>
    """
    return response

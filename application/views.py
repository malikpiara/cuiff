from bson.errors import BSONError
from flask import Blueprint, render_template, redirect, url_for, session, flash
from .forms import ChangePasswordReal, Entry, SignIn, SignUp, UserSettings, DeleteUser, ChangeName, ChangeEmail, ChangePassword, ChangePasswordReal, NewBoard
from werkzeug.security import check_password_hash
from .models import create_board, delete_entry, get_boards, get_entries, find_user_by_email, create_user, create_entry, get_entry, update_user, delete_user, update_email, update_name, update_password, get_board
from .emails import send_email
from bson.objectid import ObjectId

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
    session["username"] = None
    return redirect("/login")


@bp.route("/", methods=["GET", "POST"])
def home():
    form = NewBoard()
    if not session.get("user_id"):
        return redirect("/login")

    user_id = ObjectId(session["user_id"])
    boards = get_boards()

    if form.validate_on_submit():
        create_board(user_id,
                     form.question.data,
                     form.visibility.data.lower())
        return redirect("/")

    return render_template("page.html", boards=boards, user_id=user_id,
                           form=form)


@bp.route("/entries/<entry_id>", methods=["DELETE", "POST"])
def deleteEntry(entry_id):
    user_id = ObjectId(session["user_id"])
    entry = get_entry(ObjectId(entry_id))

    if entry["user_id"] == user_id:
        delete_entry(entry_id)

    else:
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))


@bp.route("/boards/<board_number>", methods=["GET", "POST"])
def board(board_number):
    try:
        # NOTE: converting board_number from string to ObjectId
        board_number = ObjectId(board_number)
    except BSONError:
        return redirect("/")
    form = Entry()
    user_id = ObjectId(session["user_id"])

    if form.validate_on_submit():
        create_entry(content=form.entry_input.data,
                     user_id=user_id,
                     board_id=board_number)
        return redirect(url_for('main.board', board_number=board_number))

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


""" @bp.route("/progress/<author>")
def progress(author):
    entries = get_entries()

    return render_template("progress.html", entries=entries, author=author) """

from flask import Blueprint, render_template, redirect, url_for, session
from .forms import Entry, SignIn, SignUp, UserSettings, DeleteUser
from werkzeug.security import check_password_hash
from .models import get_entries, find_user_by_email, create_user, create_entry, update_user, delete_user
from .emails import send_email

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
            # If user is found, store the email in session
            if check:
                session["username"] = email
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

        send_email("malikpiara@gmail.com", user_email, user_name)
        return redirect(url_for('main.home'))
    return render_template("signup.html", form=form)


@bp.route("/", methods=["GET", "POST"])
def home():
    if not session.get("username"):
        return redirect("/login")
    form = Entry()
    email = session["username"]
    user_information = find_user_by_email(email)
    if form.validate_on_submit():

        create_entry(content=form.entry_input.data,
                     user_id=user_information["_id"])
        return redirect(url_for('main.home'))

    # Showing entries from database on the page.
    entries = get_entries()

    return render_template("home.html", entries=entries, form=form,
                           user_information=user_information)


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = UserSettings()
    delete_user_button = DeleteUser()

    email = session["username"]
    user_information = find_user_by_email(email)

    if form.validate_on_submit():
        email = session["username"]
        new_email = form.email_address.data

        update_user(email_address=email,
                    name=form.name.data, new_email=new_email)

        session["username"] = new_email

        return redirect(url_for('main.home'))

    if delete_user_button.validate_on_submit():
        delete_user(user_id=user_information["_id"], email_address=email)
        session["username"] = None

        return redirect(url_for('main.login'))

    return render_template("settings.html",
                           user_information=user_information, form=form,
                           delete_user_button=delete_user_button, email=email)


@bp.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login")


@bp.route("/progress/<author>")
def progress(author):
    entries = get_entries()

    return render_template("progress.html", entries=entries, author=author)

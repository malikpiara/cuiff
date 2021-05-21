from flask import Blueprint, render_template, redirect, url_for, session, flash
from .forms import ChangePasswordReal, Entry, SignIn, SignUp, UserSettings, DeleteUser, ChangeName, ChangeEmail, ChangePassword, ChangePasswordReal
from werkzeug.security import check_password_hash
from .models import get_entries, find_user_by_email, create_user, create_entry, update_user, delete_user, update_email, update_name, update_password
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

        send_email("Fuzzboard | New signup", "malikpiara@gmail.com",
                   "mail/email", user_email, user_name)
        send_email("Welcome to Fuzzboard", user_email,
                   "mail/new_signup", user_email, user_name)
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

    """ # Old form
    if form.validate_on_submit():
        email = session["username"]
        new_email = form.email_address.data

        update_user(email_address=email,
                    name=form.name.data, new_email=new_email)

        session["username"] = new_email

        return redirect(url_for('main.home')) """

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


@bp.route("/progress/<author>")
def progress(author):
    entries = get_entries()

    return render_template("progress.html", entries=entries, author=author)

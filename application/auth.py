import os
from flask import Blueprint, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
from .forms import SignIn, SignUp, ResetPasswordRequestForm, ResetPasswordForm
from .models import find_user_by_email, create_user, check_invites, verify_reset_password_token, set_password
from .emails import send_email, send_password_reset_email
from .database import client

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = SignIn()
    # If we find a username stored in the session.
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

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@auth.route("/signup", methods=["GET", "POST"])
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

        send_email("Cuiff | New signup", os.environ.get('MAIL_DEFAULT_SENDER'),
                   "mail/email", user_email, user_name)
        send_email("Welcome to Cuiff", user_email,
                   "mail/new_signup", user_email, user_name)
        return redirect(url_for('main.home'))
    return render_template("auth/signup.html", form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
# BUG: When the password is reset, the token apparently still works.
# TODO: Create message that flashes when user requests a password reset.
# Do the same for when the 2 passwords don't match.
# TODO: Create email that lets the user know his password has been reset.
def reset_password(token):

    if session.get("username"):
        return redirect(url_for('main.settings'))

    user = verify_reset_password_token(token)

    if not user:
        return redirect(url_for('main.home'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        set_password(user['_id'], form.password.data)
        #flash('Your password has been reset')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
# BUG: When the email inputted by the user is not on the DB
# The page redirects the user to the homepage. This is a security issue.
# Nothing should be happening.
def reset_password_request():
    form = ResetPasswordRequestForm()

    if session.get("username"):
        return redirect(url_for('main.settings'))

    if form.validate_on_submit():
        email = form.email_address.data
        user = client.standups.users.find_one(
            {'email': form.email_address.data})

        if user:
            send_password_reset_email(email)
        # display message 'Check your email for the instructions to reset your password'.

    return render_template("auth/reset_password_request.html", form=form)

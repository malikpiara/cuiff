from flask import Blueprint, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
from .forms import SignIn, SignUp
from .models import find_user_by_email, create_user, check_invites
from .emails import send_email

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

        send_email("Cuiff | New signup", "malikpiara@gmail.com",
                   "mail/email", user_email, user_name)
        send_email("Welcome to Cuiff", user_email,
                   "mail/new_signup", user_email, user_name)
        return redirect(url_for('main.home'))
    return render_template("auth/signup.html", form=form)

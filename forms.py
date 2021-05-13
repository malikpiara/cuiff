from flask import flash, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo
from models import find_user_by_email


class Entry(FlaskForm):
    entry_input = TextAreaField("Your answer...", validators=[DataRequired()])
    post = SubmitField("Post")


class SignIn(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")
    submit = SubmitField("Login")


class SignUp(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=([DataRequired()]))
    password = PasswordField("Password", validators=[DataRequired(), EqualTo(
        "password2", message="Passwords must match.")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Create Account")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address):
            flash("Email already registered.")
            raise ValidationError('Email already registered.')


class UserSettings(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    save = SubmitField("Save")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address) and email_address != session.get("username"):
            flash("Email already being used.")
            raise ValidationError('Email already registered.')


class DeleteUser(FlaskForm):
    something = EmailField("Email", validators=[DataRequired(), Email()])
    delete_account = SubmitField("Delete Account")

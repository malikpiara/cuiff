from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
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
    password = PasswordField("Password")
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


class DeleteUser(FlaskForm):
    delete_account = SubmitField("Delete Account")

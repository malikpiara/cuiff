from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, ValidationError
from wtforms.fields import SelectField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo
from werkzeug.security import check_password_hash
from .models import find_user_by_email


class Entry(FlaskForm):
    entry_input = TextAreaField(
        "Your answer...", validators=[DataRequired()])
    create = SubmitField("Post")


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
    invite_code = StringField("Invite code", validators=[DataRequired(), Regexp(
        regex='calmworkplace', message='The invite code is not valid.')])
    submit = SubmitField("Create Account")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address):
            flash("Email already registered.")
            raise ValidationError('Email already registered.')


class ResetPasswordRequestForm(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class ChangeName(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    save = SubmitField("Save")


class ChangeEmail(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    save = SubmitField("Save")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address) and email_address != session.get("username"):
            flash("Email already being used.")
            raise ValidationError('Email already registered.')


class ChangePassword(FlaskForm):
    password_field = StringField("Password")


class ChangePasswordReal(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired()])
    save = SubmitField("Save")

    def validate_old_password(self, field):
        email_address = session.get("username")
        user = find_user_by_email(email_address)
        check_password = check_password_hash(user["password"], field.data)
        if not check_password:
            flash(
                "The old password doesn't match the one in our database. Please try again.")
            raise ValidationError(
                "Password does not match the one stored in the database.")


class UserSettings(FlaskForm):
    name = StringField(label="Display name", validators=[DataRequired()])
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    password_field = StringField("Password")
    save = SubmitField("Save")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address) and email_address != session.get("username"):
            flash("Email already being used.")
            raise ValidationError('Email already registered.')


class DeleteUser(FlaskForm):
    something = EmailField("Email", validators=[DataRequired(), Email()])
    delete_account = SubmitField("Delete Account")


class NewBoard(FlaskForm):
    question = StringField("Question", validators=[DataRequired()])
    # visibility = SelectField("Visibility", choices=['Private', 'Public'])
    space = SelectField("Space")
    create = SubmitField("Create")


class NewSpace(FlaskForm):
    name = StringField("Workspace Name", validators=[DataRequired()])
    create = SubmitField("Create")


class InviteToSpace(FlaskForm):
    email = EmailField("Invite people", validators=[DataRequired(), Email()])
    send = SubmitField("Send invite")

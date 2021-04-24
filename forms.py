from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class Entry(FlaskForm):
    entry_input = TextAreaField("Your answer...", validators=[DataRequired()])
    post = SubmitField("Post")


class SignIn(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Login")


class SignUp(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=([DataRequired()]))
    password = PasswordField("Password")
    submit = SubmitField("Create Account")


class UserSettings(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = EmailField("Email", validators=[DataRequired(), Email()])

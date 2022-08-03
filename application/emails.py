from flask_mail import Mail, Message
from flask.templating import render_template
from .models import get_reset_password_token, find_user_by_email

mail = Mail()


def send_email(subject, to, template, user_email=None, user_name=None, token: str = None):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(
        template + ".html", user_email=user_email, user_name=user_name, token=token)
    msg.html = render_template(
        template + ".html", user_name=user_name, user_email=user_email, token=token)
    mail.send(msg)


def send_password_reset_email(email: str):
    # ERROR: Object of type ObjectId is not JSON serializable.
    # I'm turning the objectID into a string. Is this a problem?
    user = find_user_by_email(email=email)
    token = get_reset_password_token(user_id=str(user['_id']))
    send_email(subject='Cuiff: Reset your password',
               to=email,
               template='mail/reset_password', token=token)

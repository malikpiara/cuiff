from flask_mail import Mail, Message
from flask.templating import render_template
#from flask import current_app
#current_app.config["FUZZBOARD_MAIL_SUBJECT_PREFIX"] = "[FUZZBOARD]"
#current_app.config["FUZZBOARD_MAIL_SENDER"] = "Malik <malikpiara@gmail.com>"

mail = Mail()


def send_email(subject, to, template, user_email, user_name):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(
        template + ".html", user_email=user_email, user_name=user_name)
    msg.html = render_template(
        template + ".html", user_name=user_name, user_email=user_email)
    mail.send(msg)

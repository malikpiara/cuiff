import os
from flask_mail import Mail, Message
from flask.templating import render_template
from flask import current_app

current_app.config["FUZZBOARD_MAIL_SUBJECT_PREFIX"] = "[FUZZBOARD]"
current_app.config["FUZZBOARD_MAIL_SENDER"] = "Malik <malikpiara@gmail.com>"


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config["FUZZBOARD_MAIL_SUBJECT_PREFIX"] + subject,
                  sender=current_app.config["FUZZBOARD_MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

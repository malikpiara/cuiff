from flask import render_template, Blueprint, redirect, url_for, session
from .models import add_active_workspace_to_user

admin = Blueprint('admin', __name__)


@admin.route('/update', methods=["GET", "POST"])
def update_db():
    """ This route enables admins to make structural changes to the DB
    like adding a new field to every document.

    Make sure to comment or remove the function after calling it in production. """

    add_active_workspace_to_user()

    return redirect(url_for('main.home'))

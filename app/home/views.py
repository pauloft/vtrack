# app/home/views.py

from flask import render_template, abort
from flask_login import current_user, login_required

from . import home


@home.route("/")
def homepage():
    """ Render homepage on the / route """
    return render_template("home/index.html", title="Welcome!")

# app/home/views.py

from flask import render_template, abort
from flask_login import current_user, login_required

from . import home


@home.route("/")
def homepage():
    """ Render homepage on the / route """
    return render_template("home/index.html", title="Welcome to VTrack!")


@home.route("/dashboard")
@login_required
def dashboard():
    """ Render dashboard on the / route """
    return render_template("home/dashboard.html", title="Your Dashboard")


@home.route("/admin_dashboard")
@login_required
def admin_dashboard():
    """ Render dashboard on the / route """
    return render_template("home/admin_dashboard.html", title="Your Dashboard")

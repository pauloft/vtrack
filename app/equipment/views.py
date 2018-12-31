# app/equipment/views.py

from flask import render_template, redirect, abort
from flask_login import current_user, login_required

from . import equipment


@equipment.route("/")
# @login_required
def index():
    return render_template("equipment/index.html", title="Equipment List")

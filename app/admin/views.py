# app/admin/views.py

from flask import render_template, abort
from flask_login import current_user, login_required

from . import admin


@admin.route("/")
# @login_required
def index():
    return render_template("admin/index.html", title="Admin")

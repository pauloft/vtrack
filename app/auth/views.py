# app/auth/views.py

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import auth
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from app.models import User


@auth.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """ Register a new user to the database using the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        # create the user
        user = User(username=form.username.data, email=form.email.data)
        # set user's password
        user.set_password(form.password.data)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash("User successfully registered - can now login.")
        # redirect to login page
        return redirect(url_for("auth.login"))

    # load registration form
    return render_template("auth/register.html", title="Register User", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """ Login users on /login route """
    if current_user.is_authenticated:
        return redirect(url_for("home.homepage"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user)
        dashboard = "home.admin_dashboard" if user.is_admin else "home.dashboard"
        return redirect(url_for(dashboard))

    return render_template("auth/login.html", title="Login", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.")

    # redirect the user to the login page
    return redirect(url_for("auth.login"))

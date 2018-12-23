# app/auth/views.py

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from . import auth
from app.auth.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from app.auth.utils import save_picture, send_reset_email
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

    return render_template("auth/login.html", title="VTrack Login", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.")

    # redirect the user to the login page
    return redirect(url_for("auth.login"))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """ View and/or update user profile """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # update the other fields from the form
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("auth.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_thumbs/" + current_user.image_file)
    return render_template(
        "auth/account.html", title="Your Profile", image_file=image_file, form=form
    )


@auth.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    """ Submit a request for changing user password """
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            f"An email sent to {form.email.data} with instructions to reset your password. NB: It may be in your spam folder!",
            "info",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/request_reset.html", title="Reset Password", form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        dashb = "home.admin_dashboard" if current_user.is_admin else "home.dashboard"
        return redirect(url_for(dashb))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That was an invalid or expired token!", "warning")
        return redirect(url_for("auth.request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset. You are able to login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth.reset_password.html", title="Reset Password", form=form)


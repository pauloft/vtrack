# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import current_user

from app.models import User


class RegistrationForm(FlaskForm):
    """ Form for creating new user accounts
    """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("confirm_password")]
    )
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Register")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError("That email is already in use!")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError("That username is already taken. Try again.")


class LoginForm(FlaskForm):
    """ Form to login user """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """ Form to update user profile """

    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update my Profile")

    def validate_username(self, username):
        """ Ignore processing the existing username """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username has already been taken. Try again.")

    def validate_email(self, email):
        """ Ignore processing the existing email """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email has already been taken. Try again.")


class RequestResetForm(FlaskForm):
    """ Form to submit email address when requesting a password reset """

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """ Verify that the email address is actually in use """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account in the database with that email.")


class ResetPasswordForm(FlaskForm):
    """ Form to reset or update user password """

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")

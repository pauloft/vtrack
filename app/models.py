# app/models

from datetime import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager

# configure a user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """ Create a user """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(120), default="default.jpg")
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """ 
        Set password to a hashed value
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<User {self.username}"


class Vehicle(db.Model):
    """ Create a Vehicle. Each vehicle has unique tag and vin """

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(20), index=True, unique=True)
    tag = db.Column(db.String(20), index=True, unique=True)
    year = db.Column(db.String(4), nullable=False)
    make = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255))

    pictures = db.relationship("Picture", backref="vehicles", lazy="dynamic")

    def __repr__(self):
        return f"<Vehicle {self.year} {self.make} {self.model} TAG: {self.tag}"


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    pictures = db.relationship("Picture", backref="equipment", lazy="dynamic")


class Picture(db.Model):
    """ Picture object represents image file for Vehicle and Equipment
    instances. Filepath is the full path to the image (which SHOULD)
    only have ONE or NO assignment at a time. i.e. Vehicle or Equipment
    """

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    filepath = db.Column(db.String(128), nullable=False)
    origpath = db.Column(db.String(128))

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"))
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"))

    def __repr__(self):
        kind = (
            "Vehicle"
            if self.vehicle_id
            else "Equipment"
            if self.equipment_id
            else "Unassigned"
        )
        return f"<{kind} Picture: {self.filepath}"

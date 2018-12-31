# app/vehicles/__init__.py

from flask import Blueprint

vehicles = Blueprint("vehicles", __name__)

from . import views

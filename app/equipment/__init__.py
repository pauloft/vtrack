# app/equipment/__init__.py

from flask import Blueprint

equipment = Blueprint("equipment", __name__)

from . import views

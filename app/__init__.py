from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager

from config import app_config

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from app import models

    # register blueprints
    from .admin import admin as admin_bp
    from .home import home as home_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(home_bp)

    """ global filters used in Jinja2 template """
    # date formatter
    @app.template_filter("datetimeformat")
    def datetimeformat(value, format="%B %d, %Y"):
        return value.strftime(format)

    # format integer with thousand separator
    @app.template_filter("numberformat")
    def numberformat(value):
        return format(int(value), ",d")

    return app

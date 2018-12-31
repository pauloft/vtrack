from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# debugging
# from flask_debugtoolbar import DebugToolbarExtension

from config import app_config

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # debugging stuff
    # tb = DebugToolbarExtension(app)

    from app import models

    # register blueprints
    from .admin import admin as admin_bp
    from .home import home as home_bp
    from .auth import auth as auth_bp
    from .equipment import equipment as equipment_bp
    from .vehicles import vehicles as vehicles_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp, url_prefix="/equipment")
    app.register_blueprint(vehicles_bp, url_prefix="/vehicles")

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

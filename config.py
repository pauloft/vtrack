import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "c832ebc5c8f34a4ddab"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    ITEMS_PER_PAGE = 6

    # configure mail
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    # picture and thumbnail folders (for profiles, Vehicles, and equipment)
    PROFILE_IMAGE_FOLDER = os.path.join(basedir, "static", "profile_thumbs")
    EQUIPMENT_IMAGE_FOLDER = os.path.join(basedir, "static", "equip_imgs")
    VEHICLE_IMAGE_FOLDER = os.path.join(basedir, "app", "static", "vehicle_imgs")


class DevelopmentConfig(Config):
    """ Development configurations """

    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "vtrack.db")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://vtrack:c832ebc5cA@localhost/vtrack"
    DEBUG = True


class ProductionConfig(Config):
    """ Production configurations """


class TestingConfig(Config):
    """ Testing configurations """

    TESTING = True


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

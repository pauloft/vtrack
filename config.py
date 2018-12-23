import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "c832ebc5c8f34a4ddab"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SEGMENTS_PER_PAGE = 20

    # configure mail
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")


class DevelopmentConfig(Config):
    """ Development configurations """

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "vtrack.db")
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

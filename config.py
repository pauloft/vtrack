import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "c832ebc5c8f34a4ddab"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SEGMENTS_PER_PAGE = 20


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

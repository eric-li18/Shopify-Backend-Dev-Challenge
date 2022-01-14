import os


class Config(object):
    """Base config"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@localhost/inventory"
    DEBUG = True


class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@postgres:5432/inventory"
    DEBUG = True


config = {"dev": DevelopmentConfig, "prod": ProductionConfig, "docker": DockerConfig}

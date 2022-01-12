import os

from flask import Flask
from api.config import config
from sqlalchemy_utils import create_database, database_exists


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        # load the test config dict if passed in
        app.config.from_mapping(test_config)
    else:
        # load the instance config from config.py
        env = os.environ.get("FLASK_APP", "dev")
        app.config.from_object(config[env])

    if env != "prod":
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_uri):
            print("Creating database with URI:" + db_uri)
            create_database(db_uri)

    from api.models import db

    db.init_app(app)
    print("Running app...")

    return app
from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def setup_app() -> object:
    """
    Creates a new Flask application
    :return: Flask object
    """
    _app = Flask(__name__)
    _app.config.from_pyfile("config.py")
    return _app


def setup_database(_app: object) -> SQLAlchemy:
    """
    Creates the new database engine inside the Flask App
    :param app: Flask App
    :return: A new database engine
    """
    _db = SQLAlchemy()
    _db.init_app(_app)
    return _db


def setup_database_migration(_app: object, _db: SQLAlchemy) -> Migrate:
    """
    Setup the database automatic migration
    :param app: Flask App
    :param db: Database Engine
    :return: Migration object
    """
    return Migrate(_app, _db)


app = setup_app()
db = setup_database(app)
migrate = setup_database_migration(app, db)
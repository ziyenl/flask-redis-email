import os
import redis
import requests

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from db import db
from resources.user import blp as UserBluePrint
from rq import Queue

def create_app(db_url=None):
    """
    Create app
    :param db_url: database url
    :return: flask app
    """
    app = Flask(__name__)

    # redis configuration
    connection = redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue("registration_emails", connection=connection)

    # configs for Swagger Documentation
    app.config["API_TITLE"] = "Redis Queue REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)  # connect flask app with sqlalchemy

    migrate = Migrate(app, db)

    # Flask smorest extension around Flask
    api = Api(app)

    # Create database schemas at first request for local development
    #with app.app_context():
        #db.create_all()

    api.register_blueprint(UserBluePrint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

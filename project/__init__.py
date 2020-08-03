from flask import Flask, request
from project.db import db
from project.ping import ping_blueprint

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # set up extensions
    db.init_app(app)

    # register blueprints
    app.register_blueprint(ping_blueprint)

    return app




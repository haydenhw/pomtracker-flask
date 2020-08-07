from flask import Flask, jsonify
from marshmallow import ValidationError
from project.projects import views
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
    app.register_blueprint(views.blueprint)

    # register error handling
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    return app




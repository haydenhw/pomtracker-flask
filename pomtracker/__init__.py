import os
from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError
from pomtracker.projects.views import ProjectList, Project
from pomtracker.tasks.views import TaskList, Task
from pomtracker.extensions import db
from pomtracker.ping import ping_blueprint

def create_app():

    # instantiate the app
    app = Flask(__name__)
    CORS(app)

    # configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # register views
    app.add_url_rule('/api/projects', view_func=ProjectList.as_view('project_list'))
    app.add_url_rule('/api/projects/<int:project_id>', view_func=Project.as_view('project'))
    app.add_url_rule('/api/tasks', view_func=TaskList.as_view('task_list'))
    app.add_url_rule('/api/tasks/<int:task_id>', view_func=Task.as_view('task'))
    app.register_blueprint(ping_blueprint)

    # register error handling
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    return app




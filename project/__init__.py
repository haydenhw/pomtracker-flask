from flask import Flask, jsonify
from marshmallow import ValidationError
from project.projects.views import ProjectList, Project
from project.tasks.views import TaskList, Task
from project.extensions import db
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
    app.add_url_rule('/projects', view_func=ProjectList.as_view('project_list'))
    app.add_url_rule('/projects/<int:project_id>', view_func=Project.as_view('project'))
    app.add_url_rule('/tasks', view_func=TaskList.as_view('task_list'))
    app.add_url_rule('/tasks/<int:task_id>', view_func=Task.as_view('task'))

    # register error handling
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    return app




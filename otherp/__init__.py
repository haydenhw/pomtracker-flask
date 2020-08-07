from flask import Flask, request
from project.models import db, Project
from project.schemas import project_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/projects/<int:project_id>')
def project_item(project_id):
    project = Project.query.filter_by(id=project_id).first()
    result = project_schema.dump(project)
    return result


@app.route('/projects', methods=['POST'])
def post_project():
    try:
        project_data = project_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    if Project.query.filter_by(text=project_data['text']).first():
        return {'message': 'Already exists in database'}, 400

    project = Project(**project_data)
    project.save_to_db()
    return {'message': 'Project Created!'}, 201


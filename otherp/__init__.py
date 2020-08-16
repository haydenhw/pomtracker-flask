from flask import Flask, request
from project.models import db, ProjectModel
from project.schemas import project_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/api/projects/<int:project_id>')
def project_item(project_id):
    project = ProjectModel.query.filter_by(id=project_id).first()
    result = project_schema.dump(project)
    return result


@app.route('/api/projects', methods=['POST'])
def post_project():
    try:
        project_data = project_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    if ProjectModel.query.filter_by(text=project_data['text']).first():
        return {'message': 'Already exists in database'}, 400

    project = ProjectModel(**project_data)
    project.save_to_db()
    return {'message': 'ProjectModel Created!'}, 201


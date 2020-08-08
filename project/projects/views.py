from flask import Blueprint, request
from flask.views import MethodView
from project.projects.models import ProjectModel
from project.projects.schemas import project_schema, projects_schema

blueprint = Blueprint('projects', __name__)

# Response Messages
PROJECT_ALREADY_EXISTS = "A project with that name already exists."
CREATED_SUCCESSFULLY = "Project created successfully."
UPDATED_SUCCESSFULLY = "Project updated successfully."
PROJECT_NOT_FOUND = "Project not found."
PROJECT_DELETED = "Project deleted."

# Routes
PROJECTS_PATH = '/projects'

class ProjectList(MethodView):
    def get(self):
        projects = ProjectModel.query.all()
        return projects_schema.dumps(projects), 200

    def post(self):
        project_data = project_schema.load(request.get_json())

        if ProjectModel.find_by_name(project_data['project_name']):
            return {'message': PROJECT_ALREADY_EXISTS}, 400

        project = ProjectModel(**project_data)
        project.save_to_db()

        return {'message': CREATED_SUCCESSFULLY+'fdsa', 'created': project_schema.dumps(project)}, 201


class Project(MethodView):
    def patch(self, project_id):
        if not project_id:
            return {'message': 'Project id must be supplied in url '}, 400

        if not ProjectModel.find_by_id(project_id):
            return {'message': PROJECT_NOT_FOUND}, 404

        update_data = project_schema.load(request.get_json())

        ProjectModel.update_by_id(update_data, project_id)
        project = ProjectModel.find_by_id(project_id)

        return {'message': UPDATED_SUCCESSFULLY, 'updated': project_schema.dumps(project)}, 200

    def delete(self, project_id):
        project = ProjectModel.find_by_id(project_id)

        if project:
            project.delete_from_db()
            return {'message': PROJECT_DELETED}, 200

        return {'message': PROJECT_NOT_FOUND}, 404










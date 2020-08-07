from flask import Blueprint, request
from project.projects.models import Project
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

@blueprint.route(PROJECTS_PATH)
def project_list():
    projects = Project.query.all()
    return projects_schema.dumps(projects), 200


@blueprint.route(PROJECTS_PATH, methods=['POST'])
def create_project():
    project_data = project_schema.load(request.get_json())

    if Project.find_by_name(project_data['project_name']):
        return {'message': PROJECT_ALREADY_EXISTS}, 400

    project = Project(**project_data)
    project.save_to_db()

    return {'message': CREATED_SUCCESSFULLY, 'created': project_schema.dumps(project)}, 201


@blueprint.route(f'{PROJECTS_PATH}/<int:project_id>', methods=['PATCH'])
def update_project(project_id):
    if not project_id:
        return {'message': 'Project id must be supplied in url '}, 400

    if not Project.find_by_id(project_id):
        return {'message': PROJECT_NOT_FOUND}, 404

    update_data = project_schema.load(request.get_json())

    Project.update_by_id(update_data, project_id)
    project = Project.find_by_id(project_id)

    return {'message': UPDATED_SUCCESSFULLY, 'updated': project_schema.dumps(project)}, 200


@blueprint.route(f'{PROJECTS_PATH}/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.find_by_id(project_id)

    if project:
        project.delete_from_db()
        return {'message': PROJECT_DELETED}, 200

    return {'message': PROJECT_NOT_FOUND}, 404








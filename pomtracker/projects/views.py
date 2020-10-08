from flask import request
from flask.views import MethodView
from pomtracker.libs.strings import gettext
from pomtracker.projects.models import ProjectModel
from pomtracker.tasks.models import TaskModel
from pomtracker.projects.schemas import project_schema, project_list_schema


class ProjectList(MethodView):
    def get(self):
        user_id = request.args.get("userid")
        if not user_id:
            return {"message": gettext("project_user_id_required")}, 400

        projects = ProjectModel.find_by_user_id(user_id)
        return project_list_schema.dumps(projects), 200

    def post(self):
        project_data = project_schema.load(request.get_json())
        project_name = project_data["project_name"]

        if ProjectModel.find_by_name(project_name):
            return {"message": gettext("project_name_exists").format(project_name)}, 400

        project = ProjectModel.create(**project_data)

        return project_schema.dumps(project), 201


class Project(MethodView):
    def patch(self, project_id):
        if not ProjectModel.find_by_id(project_id):
            return {"message": gettext("project_not_found").format(project_id)}, 404

        update_data = project_schema.load(request.get_json(), partial=True)
        updated_project = ProjectModel.update_by_id(update_data, project_id)
        return project_schema.dumps(updated_project), 200

    def delete(self, project_id):
        project = ProjectModel.find_by_id(project_id)

        if project:
            project.delete_from_db()
            return project_schema.dumps(project), 200

        return {"message": gettext("project_not_found").format(project_id)}, 404

import json
from flask import request
from flask.views import MethodView
from project.libs.strings import gettext
from project.tasks.models import TaskModel
from project.tasks.schemas import task_schema, task_list_schema

class TaskList(MethodView):
    def post(self):
        task_data = task_schema.load(request.get_json())
        task_name = task_data['task_name']

        if TaskModel.find_by_name(task_name):
            return {'message': gettext('task_name_exists').format(task_name)}, 400
        
        task = TaskModel.create(**task_data)

        return {'message': gettext('task_created'), 'created': task_schema.dump(task)}, 201

    def get(self):
        tasks = TaskModel.query.all()
        return task_list_schema.dumps(tasks), 200

class Task(MethodView):
    def patch(self, task_id):
        update_data = task_schema.load(request.get_json(), partial=True)

        if not TaskModel.find_by_id(task_id):
            return {'message': gettext('task_not_found').format(task_id)}, 404

        TaskModel.update_by_id(update_data, task_id)
        task = TaskModel.find_by_id(task_id)

        return {'message': gettext('task_updated'), 'updated': task_schema.dumps(task)}, 200

    def delete(self, task_id):
        task = TaskModel.find_by_id(task_id)

        if task:
            task.delete_from_db()
            return {'message': gettext('task_deleted')}, 200

        return {'message': gettext('task_not_found').format(task_id)}, 404


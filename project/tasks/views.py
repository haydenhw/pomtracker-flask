import json
from flask import request
from flask.views import MethodView
from project.libs.strings import gettext
from project.tasks.models import TaskModel
from project.tasks.schemas import task_schema

class TaskList(MethodView):
    def post(self):
        task_data = task_schema.load(request.get_json())
        task_name = task_data['task_name']

        if TaskModel.find_by_name(task_name):
            return {'message': gettext('task_name_exists').format(task_name)}, 400
        
        TaskModel.create(**task_data)
        return {'message': gettext('task_created')}, 201


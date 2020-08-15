import random
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel

class Factory:
    @staticmethod
    def add_project(project_name, user_id='abc123'):
        return ProjectModel.create(project_name=project_name, user_id=user_id)

    @staticmethod
    def add_task(task_name, project_id):
        return TaskModel.create(
            task_name=task_name,
            project_id=project_id,
            recorded_time=random.randrange(0, 10000),
            user_id='abc123'
        )

    @staticmethod
    def fake_project_data(project_name, user_id='abc123'):
        return dict(project_name=project_name, user_id=user_id)

    @staticmethod
    def fake_task_data(task_name, project_id):
        return dict(
            task_name=task_name,
            project_id=project_id,
            recorded_time=random.randrange(0, 10000),
            user_id='abc123'
        )

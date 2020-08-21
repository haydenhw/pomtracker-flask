import pytest
from project.tasks.models import TaskModel

def test_create_tasks_from_list(test_app, test_db, factory):
    project = factory.add_project('test project')
    task1_data = dict(task_name='task1', recorded_time=100)
    task2_data = dict(task_name='task2', recorded_time=200)
    tasks_data = [task1_data, task2_data]
    TaskModel.create_from_list(tasks_data, project.id)
    tasks = project.tasks.all()
    assert len(tasks) == 2
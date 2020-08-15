import pytest
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel
from project.tests.factory import Factory

def test_add_task(test_app, test_db):
    project = Factory.add_project('test project')
    Factory.add_task('test task', project_id=project.id)
    result = TaskModel.find_by_name('test task')
    assert result.task_name == 'test task'
    assert result.project_id == project.id
    assert type(result.recorded_time) == int

def test_makes_fake_project_data():
    project_name = 'test project'
    result = Factory.fake_project_data(project_name)
    assert result['project_name'] == project_name
    assert result['user_id'] == 1

def test_makes_fake_task_data():
    project = Factory.add_project('test project')
    task_name = 'test task'
    result = Factory.fake_task_data('test task', project_id=project.id)
    assert result['task_name'] == task_name
    assert type(result['recorded_time']) == int

def test_add_project(test_app, test_db):
    project_name = 'test project'
    Factory.add_project(project_name)
    result = ProjectModel.find_by_name(project_name)
    assert result.project_name == project_name
    assert result.user_id == 1









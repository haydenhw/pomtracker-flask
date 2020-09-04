import pytest
from pomtracker.projects.models import ProjectModel
from pomtracker.tasks.models import TaskModel
from pomtracker.tests.factory import Factory

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
    assert result['user_id'] == 'abc123'

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
    assert result.user_id == 'abc123'

def test_add_project_with_user_id(test_app, test_db):
    user_id = 'xyz456'
    project_name = 'test project'
    project = Factory.add_project(project_name=project_name, user_id=user_id)
    result = ProjectModel.find_by_id(project.id)
    assert result.project_name == project_name
    assert result.user_id == user_id








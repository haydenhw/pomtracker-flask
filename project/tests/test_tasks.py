import pytest
import json
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel

with open('project/strings/en-gb.json') as f:
    cached_strings = json.load(f)

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(TaskModel).delete()


def test_create_task(test_app, test_db):
    test_project = ProjectModel.create(project_name='project task')
    # TODO decide on calling this task_data or test_task_data
    test_task_data = dict(task_name='test task', project_id=test_project.id)
    client = test_app.test_client()
    resp = client.post(
        '/tasks',
        data=json.dumps(test_task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    task = TaskModel.find_by_name(test_task_data['task_name'])

    assert resp.status_code == 201
    assert data['message'] == cached_strings['task_created']
    assert task.task_name == test_task_data['task_name']

def test_create_task_already_exists(test_app):
    test_project = ProjectModel.create(project_name='test project')
    test_task_data = dict(task_name='Learn Django', project_id=test_project.id)
    task = TaskModel.create(**test_task_data)

    client = test_app.test_client()
    resp = client.post(
        '/tasks',
        data=json.dumps(test_task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert cached_strings['task_name_exists'].format(task.task_name) == data['message']

def test_create_task_with_null_task_name(test_app):
    test_project = ProjectModel.create(project_name='test project')
    test_task = dict(task_name=None, project_id=test_project.id)
    client = test_app.test_client()
    resp = client.post(
        '/tasks',
        data=json.dumps(test_task),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['task_name'][0] == 'Field may not be null.'


def test_create_task_with_null_project_id(test_app):
    test_task = dict(task_name='test_name', project_id=None)
    client = test_app.test_client()
    resp = client.post(
        '/tasks',
        data=json.dumps(test_task),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['project_id'][0] == 'Field may not be null.'

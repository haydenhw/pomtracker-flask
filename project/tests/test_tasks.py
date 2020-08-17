import pytest
import json
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel

with open('project/strings/en-gb.json') as f:
    cached_strings = json.load(f)

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(TaskModel).delete()


def test_create_task(test_app, test_db, factory):
    test_db.session.query(TaskModel).delete()
    project = factory.add_project('test project')
    task_name = 'test task'
    task_data = factory.fake_task_data(task_name, project.id)
    client = test_app.test_client()
    resp = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    task = TaskModel.find_by_name(task_data['task_name'])

    assert resp.status_code == 201
    assert data['message'] == cached_strings['task_created']
    assert data['created']['task_name'] == task_name
    assert task.task_name == task_name

def test_create_task_already_exists(test_app, test_db, factory):
    project = factory.add_project('test project')
    task_data = factory.fake_task_data('test task', project.id)
    task = TaskModel.create(**task_data)

    client = test_app.test_client()
    resp = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert cached_strings['task_name_exists'].format(task.task_name) == data['message']

def test_create_task_with_null_task_name(test_app, test_db, factory):
    project = factory.add_project('test project')
    task_data = factory.fake_task_data(task_name=None, project_id=project.id)
    client = test_app.test_client()
    resp = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert data['task_name'][0] == 'Field may not be null.'


def test_create_task_with_null_project_id(test_app, test_db, factory):
    task_data = factory.fake_task_data('test task', project_id=None)
    client = test_app.test_client()
    resp = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    
    assert resp.status_code == 400
    assert data['project_id'][0] == 'Field may not be null.'


# Test GET endpoint
def test_list_tasks(test_app, test_db, factory):
    project = factory.add_project('test project')
    task1 = factory.add_task('task1', project.id)
    task2 = factory.add_task('task2', project.id)

    client = test_app.test_client()
    resp = client.get('/api/tasks')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[1]['task_name'] == task2.task_name


def test_update_task(test_app, test_db, factory):
    project = factory.add_project('test project')
    task = factory.add_task('test task', project.id)

    updates = dict(task_name='updated name')
    client = test_app.test_client()
    resp = client.patch(
        f'api/tasks/{task.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )

    data = json.loads(resp.data.decode())
    updated_task = json.loads(data['updated'])

    assert resp.status_code == 200
    assert data['message'] == cached_strings['task_updated']
    assert updated_task['task_name'] == updates['task_name']
    assert updated_task['id'] == task.id


def test_update_task_invalid_json_payload(test_app, test_db, factory):
    project = factory.add_project('test project')
    task = factory.add_task('test task', project.id)

    updates = dict(task_name=None)
    client = test_app.test_client()
    resp = client.patch(
        f'api/tasks/{task.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert data['task_name'][0] == 'Field may not be null.'


def test_update_task_not_found(test_app, test_db, factory):
    updates = dict(task_name='updated name')
    test_id = 99999
    client = test_app.test_client()
    resp = client.patch(
        f'api/tasks/{test_id}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert data['message'] == cached_strings['task_not_found'].format(test_id)
    
# Test DELETE endpoint
def test_delete_task(test_app, test_db, factory):
    project = factory.add_project('test project')
    task = factory.add_task('test task', project.id)

    client = test_app.test_client()
    resp_one = client.get('/api/tasks')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"api/tasks/{task.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert data['message'] == cached_strings['task_deleted']

    resp_three = client.get('/api/tasks')
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_delete_task_not_found(test_app, test_db, factory):
    project = factory.add_project('test project')
    task = factory.add_task('test task', project.id)

    client = test_app.test_client()
    resp_one = client.get('/api/tasks')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    test_id = task.id + 999
    resp_two = client.delete(f"api/tasks/{test_id}")
    data = json.loads(resp_two.data.decode())
    assert data['message'] == cached_strings['task_not_found'].format(test_id)
    assert resp_two.status_code == 404






import json
import pytest
from pomtracker.projects.models import ProjectModel
from pomtracker.tasks.models import TaskModel

with open('pomtracker/strings/en-gb.json') as f:
    cached_strings = json.load(f)

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(TaskModel).delete()
    test_db.session.query(ProjectModel).delete()

# Test POST endpoint
def test_create_project(test_app, test_db, factory):
    project_data = factory.fake_project_data('test project')
    client = test_app.test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 201
    assert data['project_name'] == 'test project'

def test_create_project_with_tasks(test_app, test_db, factory):
    project_name = 'project with tasks'
    project_data = factory.fake_project_data(project_name)
    task1_data = dict(task_name='task1', recorded_time=100)
    task2_data = dict(task_name='task2', recorded_time=200)
    project_data['tasks'] = [task1_data, task2_data]

    client = test_app.test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    tasks = ProjectModel.find_by_name(project_name).tasks.all()
    assert resp.status_code == 201
    assert len(tasks) == 2

def test_create_project_already_exists(test_app, test_db, factory):
    project_data = factory.fake_project_data('test project')
    project = factory.add_project(**project_data)

    client = test_app.test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert cached_strings['project_name_exists'].format(project.project_name) == data['message']


def test_create_project_invalid_json_payload(test_app, test_db, factory):
    project_data = factory.fake_project_data(None)
    client = test_app.test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['project_name'][0] == 'Field may not be null.'

# Test GET endpoint
def test_list_projects(test_app, test_db, factory):
    project1 = factory.add_project('project1')
    project2 = factory.add_project('project2')
    factory.add_task('task1', project1.id)
    factory.add_task('task2', project1.id)

    client = test_app.test_client()
    resp = client.get(f'/api/projects?userid=abc123')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[1]['project_name'] == project2.project_name
    assert len(data[0]['tasks']) == 2

def test_list_projects_by_user_id(test_app, test_db, factory):
    user_id1 = 'xyz456'
    user_id2 = 'abc123'
    factory.add_project('project1', user_id=user_id1)
    factory.add_project('project2', user_id=user_id2)
    client = test_app.test_client()
    resp = client.get(f'/api/projects?userid={user_id1}')
    data = json.loads(resp.data.decode())

    assert len(data) == 1
    assert data[0]['user_id'] == user_id1

def test_list_projects_no_user_id_supplied(test_app, test_db, factory):
    client = test_app.test_client()
    resp = client.get('/api/projects')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['message'] == cached_strings['project_user_id_required']

# Test PATCH Endpoint
def test_update_project(test_app, test_db, factory):
    project = factory.add_project('test project')

    updates = dict(project_name='updated name')
    client = test_app.test_client()
    resp = client.patch(
        f'/api/projects/{project.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )

    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert data['project_name'] == updates['project_name']
    assert data['id'] == project.id


def test_update_project_invalid_json_payload(test_app, test_db, factory):
    project = factory.add_project('test project')
    updates = factory.fake_project_data(project_name=None)
    client = test_app.test_client()
    resp = client.patch(
        f'/api/projects/{project.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert data['project_name'][0] == 'Field may not be null.'


def test_update_project_not_found(test_app, test_db, factory):
    updates = factory.fake_project_data('updated name')
    test_id = 99999
    client = test_app.test_client()
    resp = client.patch(
        f'/api/projects/{test_id}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert data['message'] == cached_strings['project_not_found'].format(test_id)

# Test DELETE endpoint
def test_delete_project(test_app, test_db, factory):
    project = factory.add_project('test project')
    client = test_app.test_client()
    resp_one = client.get(f'/api/projects?userid=abc123')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/api/projects/{project.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert data['id'] == project.id

    resp_three = client.get(f'/api/projects?userid=abc123')
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_delete_project_not_found(test_app, test_db, factory):
    project = factory.add_project('test project')

    client = test_app.test_client()
    resp_one = client.get(f'/api/projects?userid=abc123')
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    test_id = project.id + 999
    resp_two = client.delete(f"/api/projects/{test_id}")
    data = json.loads(resp_two.data.decode())
    assert data['message'] == cached_strings['project_not_found'].format(test_id)
    assert resp_two.status_code == 404






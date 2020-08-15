import json
import pytest
from project.projects.views import PROJECTS_PATH
from project.projects.models import ProjectModel

with open('project/strings/en-gb.json') as f:
    cached_strings = json.load(f)

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(ProjectModel).delete()

# Test POST endpoint
def test_create_project(test_app, test_db, factory):
    project_data = factory.fake_project_data('test project')
    client = test_app.test_client()
    resp = client.post(
        PROJECTS_PATH,
        data=json.dumps(project_data),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 201
    assert cached_strings['project_created'] == data['message']


def test_create_project_already_exists(test_app, test_db, factory):
    project_data = factory.fake_project_data('test project')
    project = factory.add_project(**project_data)

    client = test_app.test_client()
    resp = client.post(
        PROJECTS_PATH,
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
        PROJECTS_PATH,
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
    task1 = factory.add_task('task1', project1.id)
    task2 = factory.add_task('task2', project1.id)

    client = test_app.test_client()
    resp = client.get(PROJECTS_PATH)
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[1]['project_name'] == project2.project_name
    assert len(data[1].tasks) == 2


# Test PATCH Endpoint
def test_update_project(test_app, test_db, factory):
    project = factory.add_project('test project')

    updates = factory.fake_project_data('updated name')
    client = test_app.test_client()
    resp = client.patch(
        f'{PROJECTS_PATH}/{project.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )

    data = json.loads(resp.data.decode())
    updated_project = json.loads(data['updated'])

    assert resp.status_code == 200
    assert data['message'] == cached_strings['project_updated']
    assert updated_project['project_name'] == updates['project_name']
    assert updated_project['id'] == project.id


def test_update_project_invalid_json_payload(test_app, test_db, factory):
    project = factory.add_project('test project')
    updates = factory.fake_project_data(project_name=None)
    client = test_app.test_client()
    resp = client.patch(
        f'{PROJECTS_PATH}/{project.id}',
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
        f'{PROJECTS_PATH}/{test_id}',
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
    resp_one = client.get(PROJECTS_PATH)
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"{PROJECTS_PATH}/{project.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert data['message'] == cached_strings['project_deleted']

    resp_three = client.get(PROJECTS_PATH)
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0

def test_delete_project_not_found(test_app, test_db, factory):
    project = factory.add_project('test project')

    client = test_app.test_client()
    resp_one = client.get(PROJECTS_PATH)
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    test_id = project.id + 999
    resp_two = client.delete(f"{PROJECTS_PATH}/{test_id}")
    data = json.loads(resp_two.data.decode())
    assert data['message'] == cached_strings['project_not_found'].format(test_id)
    assert resp_two.status_code == 404






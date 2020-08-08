import json
import pytest
from project.projects.views import \
    PROJECTS_PATH, CREATED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, PROJECT_ALREADY_EXISTS, PROJECT_NOT_FOUND
from project.projects.models import ProjectModel

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(ProjectModel).delete()

# Test POST endpoint
def test_create_project(test_app):
    test_project = dict(project_name='Learn Django')
    client = test_app.test_client()
    resp = client.post(
        PROJECTS_PATH,
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 201
    assert CREATED_SUCCESSFULLY in data['message']


def test_create_project_already_exists(test_app):
    test_project = dict(project_name='Learn Django')
    project = ProjectModel(**test_project)
    ProjectModel.save_to_db(project)

    client = test_app.test_client()
    resp = client.post(
        PROJECTS_PATH,
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert PROJECT_ALREADY_EXISTS in data['message']


def test_create_project_invalid_json_payload(test_app):
    test_project = dict(project_name=None)
    client = test_app.test_client()
    resp = client.post(
        PROJECTS_PATH,
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['project_name'][0] == 'Field may not be null.'

# Test GET endpoint
def test_list_projects(test_app, test_db):
    test_project1 = ProjectModel(project_name='Learn Django')
    test_project2 = ProjectModel(project_name='Learn Go')
    test_db.session.add_all([test_project1, test_project2])
    test_db.session.commit()

    client = test_app.test_client()
    resp = client.get(PROJECTS_PATH)
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]['project_name'] == test_project1.project_name

# Test PATCH Endpoint
def test_update_project(test_app):
    project = ProjectModel(project_name='test project')
    project.save_to_db()

    updates = dict(project_name='updated name')
    client = test_app.test_client()
    resp = client.patch(
        f'{PROJECTS_PATH}/{project.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )

    data = json.loads(resp.data.decode())
    updated_project = json.loads(data['updated'])

    assert resp.status_code == 200
    assert data['message'] == UPDATED_SUCCESSFULLY
    assert updated_project['project_name'] == updates['project_name']
    assert updated_project['id'] == project.id


def test_update_project_invalid_json_payload(test_app):
    project = ProjectModel(project_name='test project')
    project.save_to_db()

    updates = dict(project_name=None)
    client = test_app.test_client()
    resp = client.patch(
        f'{PROJECTS_PATH}/{project.id}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert data['project_name'][0] == 'Field may not be null.'


def test_update_project_not_found(test_app):
    updates = dict(project_name='updated name')
    client = test_app.test_client()
    resp = client.patch(
        f'{PROJECTS_PATH}/{99999}',
        data=json.dumps(updates),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert data['message'] == PROJECT_NOT_FOUND


def test_delete_project(test_app):
    project = ProjectModel(project_name='test project')
    project.save_to_db()

    client = test_app.test_client()
    resp_one = client.get(PROJECTS_PATH)
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"{PROJECTS_PATH}/{project.id}")
    assert resp_two.status_code == 200

    resp_three = client.get(PROJECTS_PATH)
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0

def test_delete_project_not_found(test_app):
    test_project = dict(project_name='test project')
    project = ProjectModel(**test_project)
    project.save_to_db()

    client = test_app.test_client()
    resp_one = client.get(PROJECTS_PATH)
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"{PROJECTS_PATH}/{project.id + 999}")
    assert resp_two.status_code == 404






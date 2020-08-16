import pytest
import json
from project import app
from project.models import ProjectModel, db


@pytest.fixture(scope='module')
def ctx():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield {'test_app': app, 'test_database': db}
        db.session.remove()
        db.drop_all()


def test_create_project(ctx):
    db = ctx['test_database']
    db.session.query(ProjectModel).delete()
    test_project = dict(text='Lean Django')
    client = ctx['test_app'].test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert 'message' in data
    assert 'ProjectModel Created!' == data['message']
    assert resp.status_code == 201
    db_project = ProjectModel.query.filter_by(text=test_project['text']).first()
    assert db_project is not None
    assert hasattr(db_project, 'text')
    assert db_project.text == test_project['text']


def test_create_project_invalid_text_value(ctx):
    db = ctx['test_database']
    db.session.query(ProjectModel).delete()
    test_project = dict(text=123)
    client = ctx['test_app'].test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['text'][0] == 'Not a valid string.'


def test_create_project_already_exists(ctx):
    db = ctx['test_database']
    db.session.query(ProjectModel).delete()
    project = ProjectModel(text='test_proj')
    db.session.add(project)
    db.session.commit()
    test_project = dict(text=project.text)
    client = ctx['test_app'].test_client()
    resp = client.post(
        '/api/projects',
        data=json.dumps(test_project),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400


def test_route(ctx):
    db = ctx['test_database']
    db.session.query(ProjectModel).delete()
    project = ProjectModel(text='test_proj')
    db.session.add(project)
    db.session.commit()
    res = ProjectModel.query.filter_by(text='test_proj').first()
    assert res.text == 'test_proj'
    assert res.id == 1

    client = ctx['test_app'].test_client()
    resp = client.get('/api/projects/1')
    data = json.loads(resp.data.decode())
    assert data['text'] == 'test_proj'
















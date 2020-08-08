import pytest
import json
from project import app
from project.models import db, User, Task, ProjectModel
from project.schemas import project_schema
from marshmallow import ValidationError, fields, Schema


@pytest.fixture(scope='module')
def test_database():
    with app.app_context():
        db.create_all()
        yield db
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def add_project():
    def _add_project(text):
        project = ProjectModel(text=text)
        db.session.add(project)
        db.session.commit()
        return project
    return _add_project


@pytest.fixture(scope='function')
def add_task():
    def _add_task(text, project_id):
        task = Task(text=text, project_id=project_id)
        db.session.add(task)
        db.session.commit()
        return task
    return _add_task


def test_project(test_database, add_project):
    project = add_project('Learn Django')
    res = ProjectModel.query.filter_by(text='Learn Django').first()
    assert res.text == 'Learn Django'


def test_serialize_project(test_database, add_project):
    text = 'Learn Django'
    project = add_project(text)
    _json = project_schema.dumps(project)
    assert text in _json
    _dict = json.loads(_json)
    del _dict['id']
    _dict['text'] = 123
    try:
        project = project_schema.load(_dict)
    except ValidationError as err:
        assert 'Not a valid string' in err.messages['text'][0]


def test_task(test_database, add_project, add_task):
    task = add_task(text='eat', project_id=1)
    res = Task.query.filter_by(text='eat').first()
    assert res.text == 'eat'
    assert res.project_id == 1


def test_relationship(test_database, add_project, add_task):
    test_database.session.query(Task).delete()
    test_database.session.query(ProjectModel).delete()
    add_project(text='Lean Django')
    add_task(text='eat', project_id=1)
    add_task(text='sleep', project_id=1)
    tasks = Task.query.all()
    assert len(tasks) == 2
    project = ProjectModel.query.filter_by(id=1).first()
    assert [p.id for p in project.tasks] == [1, 2]


def test_relationship_dump(test_database, add_project, add_task):
    test_database.session.query(Task).delete()
    test_database.session.query(ProjectModel).delete()
    project = add_project(text='Lean Django')
    add_task(text='eat', project_id=1)
    add_task(text='sleep', project_id=1)
    tasks = project.tasks.all()
    dumped = project_schema.dump(project)
    assert dumped['tasks'][0]['text'] == 'eat'
    assert len(dumped['tasks']) == 2
    assert dumped['text'] == 'Lean Django'

















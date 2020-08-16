import pytest
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(TaskModel).delete()
    test_db.session.query(ProjectModel).delete()

def test_find_by_user_id(test_app, test_db, factory):
    user_id1 = 'xyz456'
    user_id2 = 'abc123'
    factory.add_project('project1a', user_id=user_id1)
    factory.add_project('project1b', user_id=user_id1)
    factory.add_project('project2', user_id=user_id2)
    results = ProjectModel.find_by_user_id(user_id1)
    assert len(results) == 2

def test_project_create(test_app, test_db, factory):
    test_project_name = 'test project'
    project = factory.add_project(test_project_name)
    result = ProjectModel.find_by_name(test_project_name)
    assert result.project_name == test_project_name == project.project_name

def test_project_task_relationship(test_app, test_db, factory):
    project = factory.add_project('test project')
    factory.add_task('task1', project.id)
    factory.add_task('task2', project.id)
    assert test_db.session.query(TaskModel).filter_by(project_id=project.id).count() == 2

def test_cascade_delete_tasks(test_app, test_db, factory):
    project = factory.add_project('test project')
    factory.add_task('task1', project.id)
    factory.add_task('task2', project.id)
    result = test_db.session.query(TaskModel).all()
    assert len(result) == 2

    project.delete_from_db()
    result = test_db.session.query(TaskModel).all()
    assert len(result) == 0

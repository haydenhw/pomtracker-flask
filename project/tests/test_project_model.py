import pytest
from project.projects.models import ProjectModel
from project.tasks.models import TaskModel

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(ProjectModel).delete()
    test_db.session.query(TaskModel).delete()

def test_project_create(test_app, test_db):
    test_project_name = 'test project'
    project_data = dict(project_name=test_project_name)
    project =  ProjectModel.create(**project_data)
    result = ProjectModel.find_by_name(test_project_name)
    assert result.project_name == test_project_name == project.project_name

def test_project_task_relationship(test_app, test_db):
    project = ProjectModel(project_name='test project')
    task1 = TaskModel(task_name='task1', project_id=project.id)
    task2 = TaskModel(task_name='task2', project_id=project.id)
    project.tasks = [task1, task2]
    test_db.session.add(project)
    test_db.session.commit()
    assert test_db.session.query(TaskModel).filter_by(project_id=project.id).count() == 2
    # assert project.tasks[0].id == test_task['id']




import pytest
from project.projects.models import ProjectModel

@pytest.fixture(autouse=True)
def clear_db(test_app, test_db):
    test_db.session.query(ProjectModel).delete()

def test_project_create(test_app, test_db):
    test_project_name = 'test project'
    project_data = dict(project_name=test_project_name)
    ProjectModel.create_from_dict(project_data)
    result = ProjectModel.find_by_name(test_project_name)
    assert result.project_name == test_project_name
from  project.projects.models import ProjectModel

class Factory:
    @staticmethod
    def add_project(project_name='test project', user_id=1):
        ProjectModel.create(project_name=project_name, user_id=1)


def test_factory():
    project_name = 'test project'
    Factory.add_project()
    result = ProjectModel.find_by_name(project_name)
    assert result.name == project_name
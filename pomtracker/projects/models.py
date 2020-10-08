from datetime import datetime
from pomtracker.extensions import db, CrudMixin
from pomtracker.tasks.models import TaskModel


class ProjectModel(db.Model, CrudMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80), nullable=False)
    client_id = db.Column(db.String(80))
    user_id = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    tasks = db.relationship(
        "TaskModel",
        backref="project",
        lazy="dynamic",
        cascade="all, delete, delete-orphan",
    )

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(project_name=name).first()

    @classmethod
    def save(cls, **kwargs):
        project = cls(**kwargs)
        db.session.add(project)
        db.session.commit()
        return project

    @classmethod
    def save_with_tasks(cls, **kwargs):
        project_data = kwargs
        tasks_data = project_data["tasks"]
        project_data["tasks"] = []

        project = cls.save(**project_data)
        TaskModel.create_from_list(tasks_data, project.id)
        return project

    @classmethod
    def create(cls, **kwargs):
        project_data = kwargs
        if "tasks" in project_data:
            return cls.save_with_tasks(**kwargs)

        return cls.save(**kwargs)

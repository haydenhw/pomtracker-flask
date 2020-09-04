from datetime import datetime
from pomtracker.extensions import db
from pomtracker.extensions import CrudMixin

class TaskModel(db.Model, CrudMixin,):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    recorded_time = db.Column(db.Integer, default=0)
    client_id = db.Column(db.String(80))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    name_key = 'task_name'

    @classmethod
    def create_from_list(cls, tasks_data, project_id):
        tasks = [cls(**t, project_id=project_id) for t in tasks_data]
        db.session.add_all(tasks)
        db.session.commit()
        return tasks




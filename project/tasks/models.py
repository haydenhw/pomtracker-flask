from project.extensions import db
from project.extensions import CrudMixin

class TaskModel(db.Model, CrudMixin,):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name_key = 'task_name'






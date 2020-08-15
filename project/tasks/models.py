from datetime import datetime
from project.extensions import db
from project.extensions import CrudMixin

class TaskModel(db.Model, CrudMixin,):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    recorded_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.String(80))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.now)
    name_key = 'task_name'






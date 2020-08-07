from project.db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

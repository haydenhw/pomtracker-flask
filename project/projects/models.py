from project.extensions import db, CrudMixin

class ProjectModel(db.Model, CrudMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('TaskModel', backref='project', lazy='dynamic', cascade="all, delete, delete-orphan")
    name_key = 'project_name'




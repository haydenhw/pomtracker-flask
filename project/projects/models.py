from project.db import db

class ProjectModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80), nullable=False)
    # tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(project_name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def create_from_dict(cls, project_data):
        project = cls(**project_data)
        db.session.add(project)
        db.session.commit()

    @classmethod
    def update_by_id(cls, updates, id_):
        cls.query.filter_by(id=id_).update(updates)
        db.session.commit()


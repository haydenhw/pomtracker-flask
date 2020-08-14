from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CrudMixin:
    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_name(cls, name):
        arg_dict = {}
        arg_dict[cls.name_key] = name
        return cls.query.filter_by(**arg_dict).first()

    @classmethod
    def create(cls, **kwargs):
        project = cls(**kwargs)
        db.session.add(project)
        db.session.commit()
        return project

    @classmethod
    def update_by_id(cls, updates, id_):
        cls.query.filter_by(id=id_).update(updates)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

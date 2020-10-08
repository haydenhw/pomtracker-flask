from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CrudMixin:
    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        db.session.add(item)
        db.session.commit()
        return item

    @classmethod
    def update_by_id(cls, updates, id_):
        cls.query.filter_by(id=id_).update(updates)
        db.session.commit()
        # find the newly updated row and return it
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

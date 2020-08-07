from marshmallow import Schema, fields
from project.db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    tag = db.Column(db.Text)
    duration = db.Column(db.String)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(project_name=name).first()

# make a model
# seed an entity for the model
# get the entity
# update multiple properties of the entity

# make a marshmallow schema
# task a sample partial update dict
# validate it with a serializer

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    tag = fields.Str(required=True)
    duration = fields.Int(required=True)


task_schema = TaskSchema()


def test_update(test_app, test_db):
    task_dict = dict(name='fdsa', tag='coding', duration=300)
    task = Task(**task_dict)
    test_db.session.add(task)
    test_db.session.commit()

    # updates = dict(tag='fishing', duration=123)
    updates = dict(tag='fishing', duration=123)
    updates = task_schema.load(updates, partial=True)

    task = Task.query.filter_by(name='fdsa').first()
    test_db.session.query(Task).filter_by(name='fdsa').update(updates)
    task = Task.query.filter_by(name='fdsa').first()

    assert task.duration == 123
    assert task.tag == 'fishing'










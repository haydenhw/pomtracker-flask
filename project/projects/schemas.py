from marshmallow import Schema, fields, EXCLUDE
from project.tasks.schemas import TaskSchema


class ProjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        dump_only = ("id", "date_created")

    id = fields.Int()
    project_name = fields.Str(required=True)
    user_id = fields.Str(required=True)
    tasks = fields.List(fields.Nested(TaskSchema))
    client_id = fields.Str()
    date_created = fields.Str()


project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)


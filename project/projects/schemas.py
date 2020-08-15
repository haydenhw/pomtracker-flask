from marshmallow import Schema, fields
from project.tasks.schemas import TaskSchema


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True)
    user_id = fields.Str(required=True)
    tasks = fields.List(fields.Nested(TaskSchema))


project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)


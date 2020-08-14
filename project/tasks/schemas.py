from marshmallow import Schema, fields


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True)
    project_id = fields.Int(required=True)


task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


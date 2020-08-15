from marshmallow import Schema, fields


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True)
    recorded_time = fields.Int(required=True)
    project_id = fields.Int(required=True)
    user_id = fields.Str(required=True)


task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


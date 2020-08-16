from marshmallow import Schema, fields


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True)
    recorded_time = fields.Int(required=True)
    project_id = fields.Int(required=True)
    client_id = fields.Str()
    date_created = fields.Str(dump_only=True)


task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


from marshmallow import Schema, fields, EXCLUDE


class TaskSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        dump_only = ("id", "date_created")

    id = fields.Int()
    task_name = fields.Str(required=True)
    recorded_time = fields.Int(required=True)
    project_id = fields.Int(required=True)
    client_id = fields.Str()
    date_created = fields.Str()


task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

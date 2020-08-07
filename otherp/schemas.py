from marshmallow import Schema, fields


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str()
    project_id = fields.Int()



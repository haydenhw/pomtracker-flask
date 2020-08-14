from marshmallow import Schema, fields


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True)
    user_id = fields.Int() # TODO make required
    # tasks = fields.List(fields.Nested(TaskSchema))


project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)


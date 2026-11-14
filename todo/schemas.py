from marshmallow import Schema, ValidationError, fields
from marshmallow import pre_load, validate, validates_schema


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    done = fields.Boolean(dump_only=True)
    creation_date = fields.String(dump_only=True)

    @pre_load
    def strip_title(self, data, **kwargs):
        if not isinstance(data, dict):
            return data
        if isinstance(data.get("title"), str):
            return {**data, "title": data["title"].strip()}
        return data


class TaskPatchSchema(TaskSchema):
    done = fields.Boolean()

    @pre_load
    def strict_done(self, data, **kwargs):
        if isinstance(data, dict) and "done" in data:
            if type(data["done"]) is not bool:
                raise ValidationError({"done": ["Expected bool"]})
        return data

    @validates_schema
    def require_change(self, data, **kwargs):
        if not data:
            raise ValidationError("Provide title or done")


class ErrorSchema(Schema):
    error = fields.String()
    details = fields.Raw()

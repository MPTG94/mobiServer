from marshmallow import fields, Schema
from marshmallow.validate import Range


class ConvertImagesToVideoSchema(Schema):
    objects = fields.Int(required=False, strict=True, validate=Range(min=1), default=3)
    datetime = fields.String(required=False)

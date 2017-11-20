from marshmallow import Schema, fields


class CopernicusDataSchema(Schema):
    index = fields.Number()
    type = fields.Str()
    latitude = fields.Number()
    longitude = fields.Number()
    date = fields.DateTime()
    description = fields.Dict()
    distance = fields.Number()
    value = fields.Number()
    classification = fields.Str()

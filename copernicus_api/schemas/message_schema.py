import json

import marshmallow
from marshmallow import Schema, fields


class MessageSchema(Schema):
    message = fields.Str()
    data = fields.Dict()

    @marshmallow.post_load
    def to_json(self, data):
        return



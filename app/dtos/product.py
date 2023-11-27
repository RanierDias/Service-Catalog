from marshmallow import Schema, fields


class VariationsProductSchema(Schema):
    image = fields.String(required=True)
    value = fields.String(required=True)
    price = fields.Float(required=True)
    unit = fields.String()


class ProductSchema(Schema):
    _id = fields.String(dump_only=True)
    code = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String()
    category = fields.String(required=True)
    variations = fields.Nested(
        VariationsProductSchema, many=True, required=True)

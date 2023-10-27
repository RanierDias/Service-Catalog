from marshmallow import Schema, fields


class VariationsProductSchema(Schema):
    image = fields.String(required=True)
    value = fields.String(required=True)
    price = fields.Float(required=True)


class ProductSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    category = fields.String(required=True)
    sale_type = fields.String()
    variations = fields.Nested(
        VariationsProductSchema, many=True, required=True)

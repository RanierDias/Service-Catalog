from marshmallow import Schema, fields


class CartSchema(Schema):
    _id = fields.String(dump_only=True)
    code = fields.String(required=True)
    name = fields.String(required=True)
    image = fields.String(required=True)
    price = fields.Float(required=True)
    value = fields.String(required=True)
    amount = fields.Number(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RegisterSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.Integer(required=True)
    password = fields.String(required=True, load_only=True)
    cart = fields.Nested(CartSchema, many=True, load_only=True)

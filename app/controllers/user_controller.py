from app.services import log_user, create_user, active_user, delete_user, update_user, infor_user, cart_update
from app.dtos import LoginSchema, RegisterSchema, UserSchema, CartSchema
from flask import Blueprint, request
from marshmallow import ValidationError
import json


user_bp = Blueprint('user', __name__)
messageRequiredToken = {'message': 'É necessário o token de acesso.'}


@user_bp.route('/', methods=['GET', 'PATCH', 'DELETE'])
def rud_user():
    if not request.authorization:
        return json.dumps(messageRequiredToken), 401

    if request.method == 'GET':
        token = request.authorization.token
        data, status = infor_user(token)

        return data, status

    if request.method == 'PATCH':
        try:
            token = request.authorization.token
            user_schema = UserSchema(partial=True)
            data_validated = user_schema(request.data)
            data, status = update_user(data_validated, token)

            return data, status
        except ValidationError as err:
            return err.messages, 400

    if request.method == 'DELETE':
        token = request.authorization.token
        data, status = delete_user(token)

        return data, status


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        login_schema = LoginSchema()

        if not request.data:
            fields = login_schema.validate({})

            return json.dumps(fields), 400

        data_validated = login_schema.loads(request.data)
        data, status = log_user(data_validated)

        return data, status
    except ValidationError as err:
        return err.messages, 400


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        register_schema = RegisterSchema()

        if not request.data:
            fields = register_schema.validate({})

            return json.dumps(fields), 400

        data_validated = register_schema.loads(request.data)
        data, status = create_user(data_validated)

        return data, status
    except ValidationError as err:
        return err.messages, 400


@user_bp.route('/active', methods=['POST'])
def active_acount():
    if not request.authorization:
        return json.dumps(messageRequiredToken), 401

    token = request.authorization.token
    data, status = active_user(token)

    return data, status


@user_bp.route('/cart', methods=['PATCH'])
def update_cart():
    try:
        if not request.authorization:
            return json.dumps(messageRequiredToken), 401

        token = request.authorization.token
        cart_schema = CartSchema()

        if not request.data:
            fields = cart_schema.validate([{}], many=True)

            return json.dumps(fields), 400

        data_validated = cart_schema.loads(request.data, many=True)
        data, status = cart_update(data_validated, token)
        print("Response control: ", data)

        return data, status
    except ValidationError as err:
        return err.messages, 400

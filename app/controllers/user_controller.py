from app.services import log_user, create_user, active_user, delete_user
from app.dtos import LoginSchema, RegisterSchema
from flask import Blueprint, request
from marshmallow import ValidationError
import json


user_bp = Blueprint('user', __name__)
messageRequiredToken = {'message': 'É necessário o token de acesso.'}


@user_bp.route('/', methods=['DELETE'])
def remove_user():
    if not request.authorization:
        return json.dumps(messageRequiredToken), 401

    token = request.authorization.token
    data, status = delete_user(token)

    return data, status


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        login_schema = LoginSchema()
        data_validated = login_schema.loads(request.data)
        data, status = log_user(data_validated)

        return data, status
    except ValidationError as err:
        return [err.messages, 400]


@user_bp.route('/register', methods=["POST"])
def register():
    try:
        register_schema = RegisterSchema()
        user_validated = register_schema.loads(request.data)
        data, status = create_user(user_validated)

        return data, status
    except ValidationError as err:
        return [err.messages, 400]


@user_bp.route('/active', methods=['POST'])
def active_acount():
    if not request.authorization:
        return json.dumps(messageRequiredToken), 401

    token = request.authorization.token
    data, status = active_user(token)

    return data, status

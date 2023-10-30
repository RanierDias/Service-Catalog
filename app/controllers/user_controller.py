import json
from flask import Blueprint, request
from ..services import log_user, create_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'])
def login():
    payload = json.loads(request.data)
    response = log_user(payload)

    data, status = response

    return data, status


@user_bp.route('/register', methods=["POST"])
def register():
    payload = json.loads(request.data)
    response = create_user(payload)

    data, status = response

    return data, status

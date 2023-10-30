from marshmallow import ValidationError
from pymongo.errors import PyMongoError
from . import user_collection, LoginSchema, RegisterSchema, CartSchema
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
import os
import jwt
import json
import datetime


load_dotenv()


messageServerError = {'message': "Erro interno no servidor."}
messageNotFound = {'message': 'Usuário não existe ou senha errada.'}
messageAlreadyExists = {'message': 'Usuário já existe.'}


def log_user(data: dict):
    try:
        login_schema = LoginSchema()
        user_validated = login_schema.load(data)
        email: str = user_validated.get('email')
        password: str = user_validated.get('password')
        user_found: dict = user_collection.find_one({'email': {'$eq': email}})

        if not user_found:
            return [messageNotFound, 404]

        pass_found: str = user_found['password']
        admin: bool = user_found['admin']
        id_user = str(user_found['_id'])

        if not pbkdf2_sha256.using(salt_size=12).verify(password, pass_found):
            return [messageNotFound, 404]

        secret_key = os.getenv("SECRET_KEY")
        token: str = jwt.encode({'user': {'id': id_user, 'admin': admin}, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(5)}, secret_key, 'HS256')
        res_json = json.dumps({'token': token})

        return [res_json, 200]
    except ValidationError as err:
        return [err.messages, 400]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        print(err)
        return [json.dumps(messageServerError), 500]


def create_user(data: dict):
    try:
        register_schema = RegisterSchema()
        user_validated = register_schema.load(data)
        email: str = user_validated.get('email')
        password: str = user_validated.get('password')
        user_found: dict = user_collection.find_one({'email': {'$eq': email}})

        if user_found:
            return [messageAlreadyExists, 400]

        pass_hashed = pbkdf2_sha256.using(salt_size=12).hash(password)

        user_validated.update({'admin': False, 'password': pass_hashed})
        user_collection.insert_one(user_validated)

        res_json = register_schema.dumps(user_validated)

        return [res_json, 201]
    except ValidationError as err:
        return [err.messages, 400]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]

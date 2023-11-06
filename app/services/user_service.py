from app.extension import user_collection
from app.template import template_confirm_acount
from app.dtos import RegisterSchema
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from bson import ObjectId
import os
import jwt
import json
import smtplib


load_dotenv()


messageServerError = {'message': "Erro interno no servidor."}
messageNotFound = {'message': 'Usuário não existe ou senha errada.'}
messageAlreadyExists = {'message': 'Usuário já existe.'}
messageNotPermission = {'message': 'Você não tem permissão suficiente.'}
messageTokenExpired = {'message': 'Token expirado ou inválido.'}


def log_user(data: dict):
    try:
        email: str = data.get('email')
        password: str = data.get('password')
        user_found: dict = user_collection.find_one(
            {'email': {'$eq': email}, 'active': True})

        if not user_found:
            return [json.dumps(messageNotFound), 404]

        user_pass: str = user_found['password']
        admin: bool = user_found['admin']
        id_user = str(user_found['_id'])

        if not pbkdf2_sha256.using(salt_size=12).verify(password, user_pass):
            return [json.dumps(messageNotFound), 404]

        secret_key = os.getenv("SECRET_KEY")
        token: str = jwt.encode(
            {
                'user': {'id': id_user, 'admin': admin},
                'exp': datetime.utcnow() + timedelta(5)
            }, secret_key, 'HS256')
        res_json = json.dumps({'token': token})

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def create_user(data: dict):
    try:
        email_user: str = data.get('email')
        password: str = data.get('password')
        user_found: dict = user_collection.find_one(
            {'email': {'$eq': email_user}})

        if user_found:
            return [json.dumps(messageAlreadyExists), 409]

        pass_hashed = pbkdf2_sha256.using(salt_size=12).hash(password)
        secret_key = os.getenv("SECRET_KEY")

        data.update(
            {'admin': False, 'active': False, 'password': pass_hashed})
        user_collection.insert_one(data)
        id_user = str(data.get("_id"))
        token: str = jwt.encode(
            {
                'user': {'id': id_user},
                'exp': datetime.utcnow() + timedelta(5)
            }, secret_key, 'HS256')

        body: str = template_confirm_acount(token)
        subject: str = 'Confirmação da conta - Luxury Goods'
        email_owner = os.getenv('EMAIL')
        auth_owner = os.getenv('AUTH_EMAIL')

        email = MIMEMultipart()
        email['From'] = email_owner
        email['To'] = email_user
        email['Subject'] = subject
        email.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_owner, auth_owner)
        server.sendmail(email['From'], email['To'], email.as_string())
        server.quit()

        register_schema = RegisterSchema()
        res_json = register_schema.dumps(data)

        return [res_json, 201]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        print("Erro: ", err)
        return [json.dumps(messageServerError), 500]


def active_user(token: str):
    try:
        secret_key = os.getenv("SECRET_KEY")
        token_decoded: dict = jwt.decode(token, secret_key, ['HS256'])
        user = token_decoded["user"]
        id: str = ObjectId(user['id'])
        user_found = user_collection.find_one_and_update(
            {'_id': {'$eq': id}}, {'$set': {'active': True}},
            return_document=ReturnDocument.AFTER
        )

        if not user_found:
            return [json.dumps(messageNotFound), 404]

        res_json = json.dumps({'path': '/home'})

        return [res_json, 202]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def delete_user(token: str):
    try:
        secret_key = os.getenv("SECRET_KEY")
        token_decoded: dict = jwt.decode(token, secret_key, ['HS256'])
        user = token_decoded['user']
        time_validity = datetime.utcfromtimestamp(token_decoded['exp'])
        time_now = datetime.utcnow()

        if time_validity < time_now:
            return [json.dumps(messageTokenExpired), 498]

        id = ObjectId(user['id'])
        user_found = user_collection.find_one_and_delete({'_id': {'$eq': id}})

        if not user_found:
            return [json.dumps(messageNotFound), 404]

        return ["Not content", 204]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        print(err)
        return [json.dumps(messageServerError), 500]

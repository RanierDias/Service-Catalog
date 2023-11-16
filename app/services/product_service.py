from app.extension import product_collection
from app.dtos import ProductSchema
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
from dotenv import load_dotenv
from datetime import datetime
import json
import jwt
import os


load_dotenv()


messageServerError = {'message': "Erro interno no servidor."}
messageNotFound = {'message': 'Produto não encontrado.'}
messageNotPermission = {'message': 'Você não tem permissão suficiente.'}
messageTokenExpired = {'message': 'Token expirado ou inválido.'}


def validate_token(token: str):
    secret_key = os.getenv("SECRET_KEY")
    token_decoded: dict = jwt.decode(token, secret_key, ['HS256'])
    user = token_decoded['user']
    time_validity = datetime.utcfromtimestamp(token_decoded['exp'])
    time_now = datetime.utcnow()

    if time_validity < time_now:
        return [json.dumps(messageTokenExpired), 498]

    admin = user['admin']

    if not admin:
        return [json.dumps(messageNotPermission), 401]

    return 200


def getListProduct():
    try:
        product_schema = ProductSchema()
        product = product_collection.find()

        res_json = product_schema.dumps(product, many=True)

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def getProduct(id):
    try:
        product = product_collection.find_one({"_id": {"$eq": id}})

        if not product:
            return [json.dumps(messageNotFound), 404]

        product_schema = ProductSchema()
        res_json = product_schema.dumps(product)

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def getProductByCategory(category: str):
    try:
        product = product_collection.find({"category": category})

        if not product:
            return [json.dumps(messageNotFound), 404]

        product_schema = ProductSchema()
        res_json = product_schema.dumps(product, many=True)

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def createProduct(payload: dict, token: str):
    try:
        status_token = validate_token(token)

        if not status_token == 200:
            return status_token

        product_schema = ProductSchema()
        product_collection.insert_one(payload)
        res_json = product_schema.dumps(payload)

        return [res_json, 201]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def updateProduct(id, payload: dict, token: str):
    try:
        status_token = validate_token(token)

        if not status_token == 200:
            return status_token

        product = product_collection.find_one_and_update(
            {'_id': {'$eq': id}}, {'$set': payload},
            return_document=ReturnDocument.AFTER
        )

        if not product:
            return [json.dumps(messageNotFound), 404]

        product_schema = ProductSchema()
        res_json = product_schema.dumps(product)

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def deleteProduct(id, token: str):
    try:
        status_token = validate_token(token)

        if not status_token == 200:
            return status_token

        product = product_collection.find_one_and_delete({"_id": {'$eq': id}})

        if not product:
            return [json.dumps(messageNotFound), 404]

        return ["Not content", 204]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]

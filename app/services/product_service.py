from . import product_collection, ProductSchema
from marshmallow import ValidationError
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
import json

messageServerError = {'message': "Erro interno no servidor."}
messageNotFound = {'message': 'Produto não encontrado.'}


def getListProduct():
    try:
        product = product_collection.find()
        product_schema = ProductSchema()
        product_json = product_schema.dumps(product, many=True)

        return [product_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def getProduct(id):
    try:
        product = product_collection.find_one({"_id": {"$eq": id}})
        product_schema = ProductSchema()

        if not product:
            return [messageNotFound, 404]

        product_json = product_schema.dumps(product)

        return [product_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def createProduct(data: dict):
    try:
        product_schema = ProductSchema()
        product_validated = product_schema.load(data)

        product_collection.insert_one(product_validated)

        product_json = product_schema.dumps(product_validated)

        return [product_json, 201]
    except ValidationError as err:
        return [err.messages, 400]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def updateProduct(id, data: dict):
    try:
        product_schema = ProductSchema(partial=True)
        payload = product_schema.load(data)
        product = product_collection.find_one_and_update(
            {'_id': {'$eq': id}}, {'$set': payload},
            return_document=ReturnDocument.AFTER
        )

        if not product:
            return [json.dumps(messageNotFound), 404]

        product_json = product_schema.dumps(product)

        return [product_json, 200]

    except ValidationError as err:
        return [err.messages, 400]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def deleteProduct(id):
    try:
        product = product_collection.find_one_and_delete({"_id": {'$eq': id}})

        if not product:
            return [json.dumps(messageNotFound), 404]

        return ["Not content", 204]
    except ValidationError as err:
        return [err.messages, 400]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]

from app.extension import product_collection
from app.dtos import ProductSchema
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
import json

messageServerError = {'message': "Erro interno no servidor."}
messageNotFound = {'message': 'Produto não encontrado.'}


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
            return [messageNotFound, 404]
        
        product_schema = ProductSchema()
        res_json = product_schema.dumps(product)

        return [res_json, 200]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def createProduct(product: dict):
    try:
        product_schema = ProductSchema()
        product_collection.insert_one(product)
        res_json = product_schema.dumps(product)

        return [res_json, 201]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]


def updateProduct(id, data: dict):
    try:
        product = product_collection.find_one_and_update(
            {'_id': {'$eq': id}}, {'$set': data},
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


def deleteProduct(id):
    try:
        product = product_collection.find_one_and_delete({"_id": {'$eq': id}})

        if not product:
            return [json.dumps(messageNotFound), 404]

        return ["Not content", 204]
    except PyMongoError as err:
        return [err._message, 500]
    except Exception as err:
        return [json.dumps(messageServerError), 500]

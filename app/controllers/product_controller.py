from app.services import getListProduct, getProduct, createProduct
from app.services import updateProduct, deleteProduct
from app.dtos import ProductSchema
from marshmallow import ValidationError
from flask import Blueprint, request
from bson import ObjectId
import json


product_bp = Blueprint("product", __name__)
messageRequiredToken = {'message': 'É necessário o token de acesso.'}


@product_bp.route('/', methods=["GET", "POST"])
def cr_products():
    if request.method == "GET":
        response = getListProduct()
        data, status = response

        return data, status
    else:
        try:
            if not request.authorization:
                return json.dumps(messageRequiredToken), 401

            product_schema = ProductSchema()
            product_validated = product_schema.loads(request.data)
            token: str = request.authorization.token

            response = createProduct(product_validated, token)
            data, status = response

            return data, status
        except ValidationError as err:
            return err.messages, 400


@product_bp.before_request
def transfrom_id():
    id = request.view_args.get('id')

    if id:
        request.view_args['id'] = ObjectId(id)


@product_bp.route('/<id>', methods=['GET', 'PATCH', 'DELETE'])
def rud_product(id):
    if request.method == "GET":
        response = getProduct(id)

        data, status = response

        return data, status

    if request.method == "PATCH":
        try:
            if not request.authorization:
                return json.dumps(messageRequiredToken), 401
            
            product_schema = ProductSchema(partial=True)
            product_validated = product_schema.loads(request.data)
            token: str = request.authorization.token
            response = updateProduct(id, product_validated, token)

            data, status = response

            return data, status
        except ValidationError as err:
            return err.messages, 400

    if request.method == "DELETE":
        if not request.authorization:
            return json.dumps(messageRequiredToken), 401
        
        token: str = request.authorization.token
        response = deleteProduct(id, token)

        data, status = response

        return data, status

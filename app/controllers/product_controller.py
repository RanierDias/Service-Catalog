from app.services import getListProduct, getProduct, getProductByCategory, createProduct
from app.services import updateProduct, deleteProduct
from app.dtos import ProductSchema
from marshmallow import ValidationError
from flask import Blueprint, request, make_response
from bson import ObjectId
import json


product_bp = Blueprint("product", __name__)
messageRequiredToken = {'message': 'É necessário o token de acesso.'}


@product_bp.route('/', methods=["GET", "POST", "OPTIONS"])
def cr_products():
    if request.method == 'OPTIONS':
        response = make_response()

        response.headers["Access-Control-Allow-Methods"] = "GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.status_code = 204

        return response

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


@product_bp.route('/category/<name>', methods=["GET", "OPTIONS"])
def read_category(name):
    if request.method == 'OPTIONS':
        response = make_response()

        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "none"
        response.status_code = 204

        return response

    response = getProductByCategory(name)
    data, status = response

    return data, status


@product_bp.before_request
def transfrom_id():
    id = request.view_args.get('id')

    if id:
        request.view_args['id'] = ObjectId(id)


@product_bp.route('/<id>', methods=['GET', 'PATCH', 'DELETE', 'OPTIONS'])
def rud_product(id):
    if request.method == 'OPTIONS':
        response = make_response()

        response.headers["Access-Control-Allow-Methods"] = "GET, PATCH, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.status_code = 204

        return response

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

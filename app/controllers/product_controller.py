from app.services import getListProduct, getProduct, createProduct
from app.services import updateProduct, deleteProduct
from app.dtos import ProductSchema
from marshmallow import ValidationError
from flask import Blueprint, request
from bson import ObjectId


product_bp = Blueprint("product", __name__)


@product_bp.route('/', methods=["GET", "POST"])
def cr_products():
    if request.method == "GET":
        product_schema = ProductSchema()

        response = getListProduct()
        data, status = response

        return data, status
    else:
        try:
            product_schema = ProductSchema()
            product_validated = product_schema.loads(request.data)

            response = createProduct(product_validated)
            data, status = response

            return data, status
        except ValidationError as err:
            return [err.messages, 400]


@product_bp.before_request
def transfrom_id():
    id = request.view_args.get('id')

    if id:
        request.view_args['id'] = ObjectId(id)


@product_bp.route('/<id>', methods=['GET', 'PATCH', 'DELETE'])
def ud_product(id):
    if request.method == "GET":
        product_schema = ProductSchema()
        response = getProduct(id)

        data, status = response

        return data, status

    if request.method == "PATCH":
        try:
            product_schema = ProductSchema(partial=True)
            product_validated = product_schema.loads(request.data)
            response = updateProduct(id, product_validated)

            data, status = response

            return data, status
        except ValidationError as err:
            return [err.messages, 400]

    if request.method == "DELETE":
        product_schema = ProductSchema()
        response = deleteProduct(id)

        data, status = response

        return data, status

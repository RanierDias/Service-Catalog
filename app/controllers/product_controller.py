import json
from flask import Blueprint, request
from bson import ObjectId
from . import getListProduct, getProduct, createProduct
from . import updateProduct, deleteProduct

product_bp = Blueprint("product", __name__)


@product_bp.route('/', methods=["GET", "POST"])
def cr_products():
    if request.method == "GET":
        response = getListProduct()
        data, status = response

        return data, status
    else:
        payload: dict = json.loads(request.data)
        response = createProduct(payload)
        data, status = response

        return data, status


@product_bp.before_request
def transfrom_id():
    id = request.view_args.get('id')

    if id:
        request.view_args['id'] = ObjectId(id)


@product_bp.route('/<id>', methods=['GET', 'PATCH', 'DELETE'])
def ud_product(id):
    if request.method == "GET":
        response = getProduct(id)

        data, status = response

        return data, status

    if request.method == "PATCH":
        payload: dict = json.loads(request.data)
        response = updateProduct(id, payload)

        data, status = response

        return data, status

    if request.method == "DELETE":
        response = deleteProduct(id)

        data, status = response

        return data, status

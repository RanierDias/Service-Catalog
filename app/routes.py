from flask import Flask, request
from .services import getListProduct, createProduct, updateProduct, deleteProduct
from bson import ObjectId
import json

app = Flask(__name__)


@app.route('/products', methods=["GET", "POST"])
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


@app.route('/products/<id>', methods=["PATCH", "DELETE"])
def ud_product(id):
    if request.method == "PATCH":
        payload: dict = json.loads(request.data)
        response = updateProduct(ObjectId(id), payload)

        data, status = response

        return data, status
    else:
        response = deleteProduct(ObjectId(id))
        data, status = response

        return data, status

from flask import Blueprint, render_template, request
from app.Services.product import ProductService
from app.Schema.product import product_schema, products_schema

product = Blueprint('product', __name__, url_prefix='/api/products')
services = ProductService()

@product.route('/add_product', methods=['POST'])
def add_producto():
    product = product_schema.load(request.json)
    try:
        status_code = 201
        return product_schema.dumps(services.add_product(product)), status_code
    except:
        status_code = 400
        return product_schema.dumps(services.add_product(product)), status_code

@product.route('/delete/<int:id>', methods=['PUT'])  
def delete_product(id):
    try:
        status_code = 200
        return product_schema.dumps(services.delete_product(id)), status_code
    except:
        status_code = 404
        return product_schema.dumps(services.delete_product(id)), status_code
    
    
@product.route('/update/<int:id>',methods=['PUT'])
def update_product(id: int):
    product = product_schema.load(request.json)
    try:
        status_code = 201
        return product_schema.dumps(services.update_product(id, product)), status_code
    except:
        status_code = 404
        return product_schema.dumps(services.update_product(id, product)), status_code

@product.route('/get_by_id/<int:id>',methods=['GET'])
def get_by_id(id):
    try:
        status_code = 200
        return product_schema.dumps(services.get_product_by_id(id)), status_code
    except:
        status_code = 404
        return product_schema.dumps(services.get_product_by_id(id)), status_code


@product.route('/get_all', methods=['GET'])
def get_all():
    try:
        status_code = 200
        return products_schema.dumps(services.get_all_active()), status_code
    except:
        status_code = 404
        return product_schema.dumps(services.get_all_active()), status_code
    
@product.route('/get_all_w_d', methods=['GET'])
def get_all_with_deleted():
    try:
        status_code = 200
        return products_schema.dumps(services.get_all()), status_code
    except:
        status_code = 404
        return product_schema.dumps(services.get_all()), status_code

from flask import Blueprint, request
from app.Services.purchase import PurchaseServices
from app.Schemas.purchases import purchase_schema, purchases_schema

purchase = Blueprint('purchase', __name__, url_prefix='/api/purchase')
services = PurchaseServices()


@purchase.route('/add_purchase', methods=['POST'])
def add_purchase():
    purchase = purchase_schema.loads(request.json)
    try:
        status_code = 201
        return purchase_schema.dump(services.add_purchase(purchase)), status_code
    except:
        status_code = 400
        return purchase_schema.dumps(services.add_purchase(purchase)), status_code

@purchase.route('/delete/<int:id>', methods=['PUT'])  
def delete_purchase(id):
    try:
        status_code = 200
        return purchase_schema.dumps(services.delete_purchase(id)), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.delete_purchase(id)), status_code
    
    
@purchase.route('/update/<int:id>',methods=['PUT'])
def update_purchase(id: int):
    purchase = purchase_schema.load(request.json)
    try:
        status_code = 201
        return purchase_schema.dumps(services.update_purchase(id, purchase)), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.update_purchase(id, purchase)), status_code

@purchase.route('/get_by_id/<int:id>',methods=['GET'])
def get_by_id(id):
    try:
        status_code = 200
        return purchase_schema.dumps(services.find_by_id(id)), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.find_by_id(id)), status_code
    
@purchase.route('/get_last/',methods=['GET'])
def get_last_record():
    try:
        status_code = 200
        return purchase_schema.dumps(services.get_last_record()), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.get_last_record()), status_code

@purchase.route('/get_all', methods=['GET'])
def get_all_active():
    try:
        status_code = 200
        return purchases_schema.dumps(services.get_all_active()), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.get_all_active()), status_code
    
@purchase.route('/get_all_w_d', methods=['GET'])
def get_all():
    try:
        status_code = 200
        return purchases_schema.dumps(services.get_all()), status_code
    except:
        status_code = 404
        return purchase_schema.dumps(services.get_all()), status_code

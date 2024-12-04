from flask import Blueprint, request
from app.Services.payments import PaymentServices
from app.Schemas.payments import payment_schema, payments_schema

payment = Blueprint('payment', __name__, url_prefix='/api/payment')
services = PaymentServices()


@payment.route('/add_payment', methods=['POST'])
def add_payment():
    payment = payment_schema.loads(request.json)
    status_code = 201
    try:
        status_code = 201
        return payment_schema.dumps(services.add_payment(payment)), status_code
    except:
        status_code = 400
        return payment_schema.dumps(services.add_payment(payment)), status_code

@payment.route('/delete/<int:id>', methods=['PUT'])  
def delete_payment(id):
    try:
        status_code = 200
        return payment_schema.dumps(services.delete_payment(id)), status_code
    except:
        status_code = 404
        return payment_schema.dumps(services.delete_payment(id)), status_code
    
    
@payment.route('/update/<int:id>',methods=['PUT'])
def update_payment(id: int):
    payment = payment_schema.load(request.json)
    try:
        status_code = 201
        return payment_schema.dumps(services.update_payment(id, payment)), status_code
    except:
        status_code = 404
        return payment_schema.dumps(services.update_payment(id, payment)), status_code

@payment.route('/get_by_id/<int:id>',methods=['GET'])
def get_by_id(id):
    try:
        status_code = 200
        return payment_schema.dumps(services.find_by_id(id)), status_code
    except:
        status_code = 404
        return payment_schema.dumps(services.find_by_id(id)), status_code


@payment.route('/get_all', methods=['GET'])
def get_all_active():
    try:
        status_code = 200
        return payments_schema.dumps(services.get_all_active()), status_code
    except:
        status_code = 404
        return payment_schema.dumps(services.get_all_active()), status_code
    
@payment.route('/get_all_w_d', methods=['GET'])
def get_all():
    try:
        status_code = 200
        return payments_schema.dumps(services.get_all()), status_code
    except:
        status_code = 404
        return payment_schema.dumps(services.get_all()), status_code

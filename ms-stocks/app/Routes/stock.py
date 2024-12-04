from flask import Blueprint, request
from app.Services.stock import StockServices
from app.Schemas.stock import stock_schema, stocks_schema

stock = Blueprint('stock', __name__, url_prefix='/api/stock')
services = StockServices()


@stock.route('/add_stock', methods=['POST'])
def add_stock():
    stock = stock_schema.loads(request.json)
    try:
        status_code = 201
        return stock_schema.dumps(services.add_stock(stock)), status_code
    except:
        status_code = 400
        return stock_schema.dumps(services.add_stock(stock)), status_code

@stock.route('/delete/<int:id>', methods=['PUT'])  
def delete_stock(id):
    try:
        status_code = 200
        return stock_schema.dumps(services.delete_stock(id)), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.delete_stock(id)), status_code
    
    
@stock.route('/update/<int:id>',methods=['PUT'])
def update_stock(id: int):
    stock = stock_schema.loads(request.json)
    try:
        status_code = 201
        return stock_schema.dumps(services.update_stock(id, stock)), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.update_stock(id, stock)), status_code

@stock.route('/get_by_id/<int:id>',methods=['GET'])
def get_by_id(id):
    try:
        status_code = 200
        return stock_schema.dumps(services.find_by_id(id)), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.find_by_id(id)), status_code

@stock.route('get_by_product/<int:id>',methods=['GET'])
def get_by_product_id(id):
    try:
        status_code = 200
        return stock_schema.dumps(services.find_by_product_id(id)), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.find_by_product_id(id)), status_code


@stock.route('/get_all', methods=['GET'])
def get_all_active():
    try:
        status_code = 200
        return stocks_schema.dumps(services.get_all_active()), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.get_all_active()), status_code
    
@stock.route('/get_all_w_d', methods=['GET'])
def get_all():
    try:
        status_code = 200
        return stocks_schema.dumps(services.get_all()), status_code
    except:
        status_code = 404
        return stock_schema.dumps(services.get_all()), status_code

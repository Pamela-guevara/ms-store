from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.Models.stock import Stock
from app.Services.format_logs import format_logs

logging = format_logs('StockRepository')

class StockRepository:

    def add_stock(self, stock: Stock) -> Stock:
        try:
            db.session.add(stock) 
            db.session.commit()
            logging.info(f'Stock {stock.id_stock} added successfully')
            return stock
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Stock {stock.id_stock} cannot save, error {e}')
            raise e
        
    def update_stock(self, stock: Stock) -> Stock:
        try:
            db.session.add(stock)
            db.session.commit()
            logging.info(f'Stock {stock.id_stock} updated successfully')
            return stock
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Stock {stock.id_stock} cannot update, error {e}')
            raise e        
            
    def find_by_id(self, id: int) -> Stock :
        try:
            res = db.session.query(Stock).filter(Stock.id_stock == id).one()
            logging.info(f'Stock with id {id} found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Stock id {id} not found, error {e}')
            raise e
        
    def find_by_product_id(self, id_product: int) -> Stock:
        try:
            res = db.session.query(Stock).filter(Stock.id_product == id_product).one_or_none()
            logging.info(f'Stock where id_product {id} found succefully')
            return res
        except NoResultFound as e:
            logging.info(f'Stocks where id_product {id} not found, error {e}')
            raise e


    def find_by_id_in(self, id:int) -> list[Stock]:
        try:
            res = db.session.query(Stock).filter_by(Stock.id_product == id, Stock.in_out == 1).all()
            logging.info(f'Stocks_in where id_product {id} found succefully')
            return res
        except NoResultFound as e:
            logging.info(f'Stocks_in where id_product {id} not found, error {e}')
            raise e
        
    def find_by_id_out(self, id:int) -> list[Stock]:
        try:
            res = db.session.query(Stock).filter_by(Stock.id_product == id, Stock.in_out == 2).all()
            logging.info(f'Stocks_out where id_product {id} found succefully')
            return res
        except NoResultFound as e:
            logging.info(f'Stocks_out where id_product {id} not found, error {e}')
            raise e
    
    def get_all_active(self) -> list[Stock]:
        try:
            res = db.session.query(Stock).filter_by(active=True).all()
            logging.info(f'All active stocks found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Avtive stock list not found, error {e}')
            raise e  
    
    def get_all(self) -> list[Stock]:
        try:
            res = db.session.query(Stock).order_by(Stock.id_stock).all()
            logging.info(f'All stocks found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Stock list not found, error {e}')
            raise e    
import logging
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.Models.purchases import Purchase
from app.Services.format_logs import format_logs

logging = format_logs('PurchasesRepository')

class PurchaseRepository:

    def add_purchase(self, purchase: Purchase) -> Purchase:
        try:
            db.session.add(purchase) 
            db.session.commit()
            logging.info(f'Purchase {purchase.id_purchase} added successfully')
            return purchase
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Purchase {purchase.id_purchase} cannot save, error {e}')
            raise e
        
    def update_purchase(self, purchase: Purchase) -> Purchase:
        try:
            db.session.add(purchase)
            db.session.commit()
            logging.info(f'Purchase {purchase.id_purchase} updated successfully')
            return purchase
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Purchase {purchase.id_purchase} cannot update, error {e}')
            raise e        
            
    def find_by_id(self, id: int) -> Purchase :
        try:
            res = db.session.query(Purchase).filter(Purchase.id_purchase == id).one()
            logging.info(f'Purchase with id {id} found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Purchase id {id} not found, error {e}')
            raise e
    
    def get_last_record(self) -> Purchase:
        try:
            res = db.session.query(Purchase).order_by(Purchase.id_purchase.desc()).first()
            logging.info(f'Last purchase found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'No purchases found, error {e}')
            raise e

    def get_all_active(self) -> list[Purchase]:
        try:
            res = db.session.query(Purchase).filter_by(deleted=False).all()
            logging.info(f'All active purchases found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Avtive Purchase list not found, error {e}')
            raise e  

    def get_all(self) -> list[Purchase]:
        try:
            res = db.session.query(Purchase).order_by(Purchase.id_purchase).all()
            logging.info(f'All purchases found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Purchase list not found, error {e}')
            raise e    
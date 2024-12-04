import logging
from app import cache
from app.Models.purchases import Purchase
from app.Repositories.purchases import PurchaseRepository
from .format_logs import format_logs
from dataclasses import dataclass

logging = format_logs('PurchaseServices')

@dataclass
class PurchaseServices():
    repository = PurchaseRepository()

    def add_purchase(self, args: dict) -> Purchase:
        purchase = Purchase()
        for key, value in args.items():
            setattr(purchase, key, value) if hasattr(purchase, key) else logging.warning("Unknown attr in add_purchase")

        cache.set(f'purchase_{purchase.id_purchase}', purchase, timeout=60)
        logging.info(f'Purchase_{purchase.id_purchase} added to cache') 

        return self.repository.add_purchase(purchase)

    def update_purchase(self, id_purchase:int, args:dict) -> Purchase:
        purchase = self.repository.find_by_id(id_purchase)
        if purchase:
            for key, value in args.items():
                setattr(purchase, key, value) if hasattr(purchase, key) else logging.warning("Unknown attr in add_purchase")
                
            cache.set(f'purchase_{id_purchase}', purchase, timeout=60)
            logging.info(f'purchase_{purchase.id_purchase} added to cache')

            return self.repository.update_purchase(purchase)
        
        logging.error("Unknown purchase to update")
        return purchase

    def delete_purchase(self, id_purchase: int) -> None:
        purchase = self.repository.find_by_id(id_purchase)
        if purchase:
            purchase.deleted = True
            cache.delete(f'purchase_{id_purchase}')
            logging.info(f'purchase_{purchase.id_purchase} deleted to cache')
            self.repository.update_purchase(purchase)
            return None
            
        logging.error("Unknown purchase to delete")
        return purchase

    def get_last_record(self) -> Purchase:
        purchase = self.repository.get_last_record()
        if purchase:
            logging.info('Last record found')
            return purchase
        else:
            logging.error('No records found')
            raise BaseException('Last record not found')

    def find_by_id(self, id_purchase: int) -> Purchase:
        purchase = cache.get(f'purchase_{id_purchase}')
        if purchase is None:
            purchase = self.repository.find_by_id(id_purchase)
            cache.set(f'purchase_{id_purchase}', purchase, timeout=60)
            logging.info(f'purchase_{purchase.id_purchase} added to cache')

        logging.info(f'purchase_{purchase.id_purchase} retrieved to cache')    
        return purchase

    def get_all_active(self) -> list[Purchase]:
        purchase = cache.get('active_purchase_list')
        if purchase is None:
            purchase = self.repository.get_all_active()
            cache.set('active_purchases_list', purchase, timeout=60)
            logging.info('All active purchases found has been added to cache successfully')

        logging.info('All active purchases found successfully from cache')    
        return purchase

    def get_all(self) -> list[Purchase]:
            purchase = cache.get('purchase_list_w_d')
            if purchase is None:
                purchase = self.repository.get_all()
                cache.set('purchase_list_w_d', purchase, timeout=60)
                logging.info('All spurchases found has been added to cache successfully')

            logging.info('All purchases found successfully from cache')
            return purchase
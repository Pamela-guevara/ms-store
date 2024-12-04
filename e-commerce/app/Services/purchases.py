import os, requests, logging
from app import cache
from app.Services.format_logs import format_logs
from app.Models.purchases import Purchase
from app.Schemas.purchases import purchase_schema, purchases_schema
from app.Models.product import Product
from app.Schemas.product import product_schema, products_schema

logging = format_logs('LinkedPurchasesService')

class LinkedPurchase:
    def __init__(self):
        self.url = os.getenv('PURCHASES_URL')
        self.purchase = Purchase()

    def buy(self, product: Product, address: str) -> None:
        
        if isinstance(self.purchase, Purchase):
            self.purchase.id_product = product.id_product
            self.purchase.shipping_address = address
        else:
            self.purchase['id_product'] = product.id_product
            self.purchase['shipping_address'] = address
        body = purchase_schema.dumps(self.purchase) #JSON
        res = requests.post(f'{self.url}/add_purchase', json=body)
        
        if res.status_code == 201:
            self.purchase = purchase_schema.loads(res.content)
            cache.set(f"purchase_{self.purchase['purchase_date']}", self.purchase)
            logging.info(f"Purchase succefully: {self.purchase['purchase_date']}\n{self.purchase} ")
            self.purchase = Purchase()
        else:
            logging.error('Error in purchase-ms trying to buy')
            raise BaseException('Error in purchase-ms trying to buy')
        
    def cancel_purchase(self) -> None:
        if isinstance(self.purchase, Purchase):
            if cache.get(f"purchase_{self.purchase.purchase_date}"):
                cache.delete(f"purchase_{self.purchase.purchase_date}")
        else:
            if cache.get(f"purchase_{self.purchase['purchase_date']}"):
                cache.delete(f"purchase_{self.purchase['purchase_date']}")

        info = requests.get(f'{self.url}/get_last')
        if info.status_code == 200:
            res = requests.put(f"{self.url}/delete/{info['purchase_date']}")
            if res.status_code == 200:
                logging.info(f"Purchase id: {info['purchase_date']} succefully cancelled")
            else:
                logging.error('Error in purchase-ms trying to cancel purchase')
                raise BaseException('Error in purchase-ms trying to cancel purchase')


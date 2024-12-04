import os, logging, requests # type: ignore
from dataclasses import dataclass
from app import cache
from app.Services.format_logs import format_logs
from app.Models.payments import Payment
from app.Schemas.payments import payment_schema
from app.Models.product import Product


logging = format_logs('LinkedPaymentService')

@dataclass
class LinkedPayment:
    url = os.getenv('PAYMENTS_URL')
    payment = Payment()

    def registry_payment(self, product: Product, payment_method: str) -> None:
        
        if isinstance(self.payment, Payment):
            self.payment.id_product = product.id_product
            self.payment.amount =  product.price
            self.payment.payment_mode = payment_method
        else:
            self.payment['id_product'] = product.id_product
            self.payment['amount'] =  product.price
            self.payment['payment_mode'] = payment_method

        body = payment_schema.dumps(self.payment)
        res = requests.post(f'{self.url}/add_payment', json=body)

        if res.status_code == 201:
            self.payment = payment_schema.loads(res.content)
            cache.set(f"payment_{self.payment['id_payment']}", self.payment)
            logging.info(f"Payment id: {self.payment['id_payment']} registered successfully\n{self.payment}")
            self.payment = Payment()
        else:
            logging.error('Error in payment-ms')
            raise BaseException('Error in payment-ms')
        
    def cancel_payment(self)-> None:
        if not self.payment.id_payment:
            logging.error('ID is needed to cancel payment')
            raise BaseException('ID is needed to cancel payment')
        
        if cache.get(f'payment_{self.payment.id_payment}'):
            cache.delete(f'payment_{self.payment.id_payment}')
        
        res = requests.put(f'{self.URL}/delete/{self.payment.id_payment}')
        if res.status_code == 200:
            logging.info(f"Payment ID: {self.compra.id} has been deleted")
        else:
            logging.error('Error in payment-ms in compensation')
            raise BaseException('Error in payment-ms in compensation')
from app import cache
from app.Models.payments import Payment
from app.Repositories.payments import PaymentRepository
from .format_logs import format_logs
from dataclasses import dataclass

logging = format_logs('PaymentServices')

@dataclass
class PaymentServices():
    repository = PaymentRepository()

    def add_payment(self, args: dict) -> Payment:
        payment = Payment()
        for key, value in args.items():
            if not payment.id_payment:
                setattr(payment, key, value) if hasattr(payment, key) else logging.warning("Unknown attr in add_payment")

        cache.set(f'payment_{payment.id_payment}', payment, timeout=60)
        logging.info(f'Payment_{payment.id_payment} added to cache')  
        return self.repository.add_payment(payment)

    def update_payment(self, id_payment:int, args:dict) -> Payment:
        payment = self.repository.find_by_id(id_payment)
        if payment:
            for key, value in args.items():
                setattr(payment, key, value) if hasattr(payment, key) else logging.warning("Unknown attr in add_payment")
                
            cache.set(f'payment_{id_payment}', payment, timeout=60)
            logging.info(f'payment_{payment.id_payment} added to cache')
            return self.repository.update_payment(payment)
        logging.error("Unknown payment to update")
        return payment

    def delete_payment(self, id_payment: int) -> None:
        payment = self.repository.find_by_id(id_payment)
        if payment:
            payment.active = False
            cache.delete(f'payment_{id_payment}')
            logging.info(f'payment_{payment.id_payment} deleted to cache')
            self.repository.update_payment(payment)
            return None
            
        logging.error("Unknown payment to delete")
        return payment

    def find_by_id(self, id_payment: int) -> Payment:
        payment = cache.get(f'payment_{id_payment}')
        if payment is None:
            payment = self.repository.find_by_id(id_payment)
            cache.set(f'payment_{id_payment}', payment, timeout=60)
            logging.info(f'payment_{payment.id_payment} added to cache')

        logging.info(f'payment_{payment.id_payment} retrieved to cache')    
        return payment

    def get_all_active(self) -> list[Payment]:
        payment = cache.get('active_payments_list')
        if payment is None:
            payment = self.repository.get_all_active()
            cache.set('active_payments_list', payment, timeout=60)
            logging.info('All active payments found has been added to cache successfully')

        logging.info('All active payments found successfully from cache')    
        return payment

    def get_all(self) -> list[Payment]:
            payment = cache.get('payments_list_w_d')
            if payment is None:
                payment = self.repository.get_all()
                cache.set('payments_list_w_d', payment, timeout=60)
                logging.info('All payments found has been added to cache successfully')

            logging.info('All payments found successfully from cache')
            return payment
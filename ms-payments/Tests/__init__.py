import unittest
from app import create_app, db
from app.Services.payments import PaymentServices

class BaseTestClass(unittest.TestCase):


    def setUp(self) -> None:
        
        self.payment_1 = {
            "id_product": 1,
            "amount": 2,
            "payment_mode": "Credit Card",
            "active": True
        }
        self.payment_2 = {
            "id_product": 2,
            "amount": 2.5,
            "payment_mode": "Cash",
            "active": False
        }
        self.payment_3 = {
            "id_product": 3,
            "amount": 3.5,
            "payment_mode": "Debit card",
            "active": True
        }
        self.payment_4 = {
            "id_product": 4,
            "amount": 1.5,
            "payment_mode": "Cash",
            "active": False
        }
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.pay_1 = self.add_payment(self.payment_1)
        self.pay_2 = self.add_payment(self.payment_2)
        self.pay_3 = self.add_payment(self.payment_3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def add_payment(payment: dict):
        service = PaymentServices()
        return service.add_payment(payment)

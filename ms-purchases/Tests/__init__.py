import unittest
from app import create_app, db
from app.Services.purchase import PurchaseServices


class BaseTestClass(unittest.TestCase):


    def setUp(self) -> None:
        
        self.purchase_1 = {
            "id_product": 1,
            "shipping_address": "Calle Falsa 123",
            "deleted": True
        }
        self.purchase_2 = {
            "id_product": 2,
            "shipping_address": "Calle Falsa 1234"
        }
        self.purchase_3 = {
            "id_product": 3,
            "shipping_address": "Calle Falsa 12345",
            "deleted": True
        }
        self.purchase_4 = {
            "id_product": 4,
            "shipping_address": "Calle Falsa 123456"
        }
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.pur_1 = self.add_purchase(self.purchase_1)
        self.pur_2 = self.add_purchase(self.purchase_2)
        self.pur_3 = self.add_purchase(self.purchase_3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def add_purchase(purchase: dict):
        service = PurchaseServices()
        return service.add_purchase(purchase)

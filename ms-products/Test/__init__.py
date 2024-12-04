import unittest
from app import create_app, db
from app.Services.product import ProductService


class BaseTestClass(unittest.TestCase):


    def setUp(self) -> None:
        
        self.product_1 = {
            "name": "Potatoes",
            "price": 10.99,
            "active": True
        }
        self.product_2 = {
            "name": "Tomatoes",
            "price": 9.99,
            "active": False
        }
        self.product_3 = {
            "name": "Lettuce",
            "price": 5.99,
            "active": True
        }
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.prod_1 = self.add_product(self.product_1)
        self.prod_2 = self.add_product(self.product_2)
        self.prod_3 = self.add_product(self.product_3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def add_product(product: dict):
        service = ProductService()
        return service.add_product(product)

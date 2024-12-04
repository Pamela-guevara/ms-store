import unittest
from app import create_app, db
from app.Services.stock import StockServices


class BaseTestClass(unittest.TestCase):


    def setUp(self) -> None:
        
        self.stock_1 = {
            "id_product": 1,
            "quantity": 2,
            "in_out": 1,
            "active": True
        }
        self.stock_2 = {
            "id_product": 2,
            "quantity": 2.5,
            "in_out": 2,
            "active": False
        }
        self.stock_3 = {
            "id_product": 3,
            "quantity": 3.5,
            "in_out": 1,
            "active": True
        }
        self.stock_4 = {
            "id_product": 4,
            "quantity": 1.5,
            "in_out": 2,
            "active": False
        }
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.stk_1 = self.add_stock(self.stock_1)
        self.stk_2 = self.add_stock(self.stock_2)
        self.stk_3 = self.add_stock(self.stock_3)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def add_stock(stock: dict):
        service = StockServices()
        return service.add_stock(stock)

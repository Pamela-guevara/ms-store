import unittest
from app.Services.stock import StockServices
from . import BaseTestClass

class StockTestCase(BaseTestClass):

    service = StockServices()

    def test_add_stock(self):
        stock = self.service.add_stock(self.stock_4)

        for key in self.stock_4.keys():
            self.assertEqual(self.stock_4[key], getattr(stock, key))
    
    def test_update_stock(self):
        stock = self.service.update_stock(2, self.stock_4)
        for key in self.stock_4.keys():
            self.assertEqual(self.stock_4[key], getattr(stock, key))

    def test_get_by_id(self):
        stock = self.service.find_by_id(3)

        for key in self.stock_3.keys():
            self.assertEqual(self.stock_3[key], getattr(stock, key))

    def test_get_all_active(self):
        stock_list = self.service.get_all_active()
        for key in self.stock_1.keys():
            self.assertEqual(self.stock_1[key], getattr(stock_list[0], key))

    def test_get_all(self):
        stock_list = self.service.get_all()
        for key in self.stock_2.keys():
            self.assertEqual(self.stock_2[key], getattr(stock_list[1], key))

    def test_delete_stock(self):
        stock = self.service.delete_stock(1)
        self.assertIsNone(stock)


if __name__ == '__main__':
    unittest.main()
    
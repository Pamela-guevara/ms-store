import unittest
#from flask import jsonify
from app.Services.product import ProductService
from . import BaseTestClass

class ProductTestCase(BaseTestClass):

    service = ProductService()

    def test_add_product(self):
        product = self.service.add_product(self.product_3)
        for key in self.product_3.keys():
            self.assertEqual(self.product_3[key], getattr(product, key))
    
    def test_update_product(self):
        product = self.service.update_product(2, self.product_3)
        for key in self.product_3.keys():
            self.assertEqual(self.product_3[key], getattr(product, key))

    def test_get_by_id(self):
        product = self.service.get_product_by_id(3)

        for key in self.product_3.keys():
            self.assertEqual(self.product_3[key], getattr(product, key))

    def test_get_all(self):
        product_list = self.service.get_all()
        for key in self.product_1.keys():
            self.assertEqual(self.product_1[key], getattr(product_list[0], key))

    def test_delete_product(self):
        res = self.service.delete_product(1)
        self.assertEqual(res.active, False)


if __name__ == '__main__':
    unittest.main()
    
import unittest
from app.Services.purchase import PurchaseServices
from . import BaseTestClass

class PurchaseTestCase(BaseTestClass):

    service = PurchaseServices()

    def test_add_purchase(self):
        purchase = self.service.add_purchase(self.purchase_4)

        for key in self.purchase_4.keys():
            self.assertEqual(self.purchase_4[key], getattr(purchase, key))
    
    def test_update_purchase(self):
        purchase = self.service.update_purchase(2, self.purchase_4)
        for key in self.purchase_4.keys():
            self.assertEqual(self.purchase_4[key], getattr(purchase, key))

    def test_get_by_id(self):
        purchase = self.service.find_by_id(3)

        for key in self.purchase_3.keys():
            self.assertEqual(self.purchase_3[key], getattr(purchase, key))

    def test_get_all_active(self):
        purchase_list = self.service.get_all_active()
        for key in self.purchase_2.keys():
            self.assertEqual(self.purchase_2[key], getattr(purchase_list[0], key))

    def test_get_all(self):
        purchase_list = self.service.get_all()
        for key in self.purchase_2.keys():
            self.assertEqual(self.purchase_2[key], getattr(purchase_list[1], key))

    def test_delete_purchase(self):
        purchase = self.service.delete_purchase(1)
        self.assertIsNone(purchase)


if __name__ == '__main__':
    unittest.main()
    
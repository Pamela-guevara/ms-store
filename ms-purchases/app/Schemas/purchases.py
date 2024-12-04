from app import ma
from marshmallow import fields, Schema, post_load
from app.Models.purchases import Purchase

class PurchaseSchema(ma.Schema):
    # id_purchase = fields.Integer(dump_only=True)
    # id_product = fields.Integer()
    # purchase_date = fields.DateTime()
    # shipping_address = fields.String()
    # active = fields.Boolean()
    # deleted = fields.Boolean()
    class Meta:
        fields = ('id_product', 'purchase_date', 'shipping_address', 'active', 'deleted')

# @post_load
# def make_purchase(self, data, **kwargs):
#     return Purchase(**data)

purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
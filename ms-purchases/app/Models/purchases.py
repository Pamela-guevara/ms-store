from app import db
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Purchase(db.Model):
    __tablename__ = 'purchases'
    __table_args__ = {'schema':'ms_purchases'}
    
    id_purchase = db.Column('id_purchase', db.Integer, primary_key=True, autoincrement=True)
    id_product = db.Column('id_product', db.Integer, nullable=False)
    purchase_date = db.Column('purchase_date', db.DateTime(timezone=True), default=func.now())
    shipping_address = db.Column('shipping_address', db.String(200), nullable=False)
    active = db.Column('active', db.Boolean, default=True)
    deleted = db.Column('deleted', db.Boolean, default=False)
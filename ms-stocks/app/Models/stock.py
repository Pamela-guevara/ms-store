from app import db
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Stock(db.Model):
    __tablename__ = 'stocks'
    __table_args__ = {'schema':'ms_stocks'}
    
    id_stock = db.Column('id_stock', db.Integer, primary_key=True, autoincrement=True)
    id_product = db.Column('id_product', db.Integer, nullable=False)
    transaction_date = db.Column('transaction_date', db.DateTime(timezone=True), default=func.now())
    quantity = db.Column('quantity', db.Float, nullable=False)
    in_out = db.Column('in_out', db.Integer, nullable=False)
    active = db.Column('active', db.Boolean, default=True)
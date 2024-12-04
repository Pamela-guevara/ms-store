from app import db
from dataclasses import dataclass

@dataclass
class Payment(db.Model):
    __tablename__ = 'payments'
    __table_args__ = {'schema':'ms_payments'}
    
    id_payment = db.Column('id_payment', db.Integer, primary_key=True, autoincrement=True)
    id_product = db.Column('id_product', db.Integer, nullable=False)
    amount = db.Column('amount', db.Float, nullable=False)
    payment_mode = db.Column('payment_mode', db.String(50), nullable=False)
    active = db.Column('active', db.Boolean, default=True)
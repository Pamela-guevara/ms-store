from app import db

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'ms_products'}
    id_product = db.Column('id_product', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(100), nullable=False)
    price = db.Column('price', db.Float, nullable=False)
    active = db.Column('active', db.Boolean, default=True, nullable=False)
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.Models.product import Product
from app.Services.format_logs import format_logs

logging = format_logs('ProductRepository')

class ProductRepository:

    def add(self, product: Product) -> Product:
        try:
            db.session.add(product) 
            db.session.commit()
            logging.info(f'Product {product.name} added successfully')
            return product
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Product {product.name} cannot save, error {e}')
            return e
        
    def update(self, product: Product) -> Product:
        try:
            db.session.add(product)
            db.session.commit()
            logging.info(f'Product {product.name} updated successfully')
            return product
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f'Product {product.name} cannot update, error {e}')
            return e        
            
            
    def find_by_id(self, id: int) -> Product :
        try:
            res = db.session.query(Product).filter(Product.id_product == id).one()
            logging.info(f'Product with id {id} found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Product id {id} not found, error {e}')
            return e
    
    def get_all_active(self) -> list[Product]:
        try:
            res = db.session.query(Product).filter_by(active=True).all()
            logging.info('All active products found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Product list not found, error {e}')
            return e        
        
    def get_all(self) -> list[Product]:
        try:
            res = db.session.query(Product).order_by(Product.id_product).all()
            logging.info('All products found successfully')
            return res
        except NoResultFound as e:
            logging.error(f'Product list not found, error {e}')
            return e
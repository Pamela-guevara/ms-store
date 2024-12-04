from app import cache
from app.Models.product import Product
from app.Repositories.product import ProductRepository
from app.Services.format_logs import format_logs
from dataclasses import dataclass

logging = format_logs('ProductServices')

@dataclass
class ProductService:  
    
    repository = ProductRepository()  

    def add_product(self, args: dict) -> Product:
        product = Product()
        for key, value in args.items():
            setattr(product, key, value) if hasattr(product, key) else logging.warning("Unknown attr in add_prod")

        cache.set(f'product_{product.id_product}', product, timeout=60)
        logging.info(f'product_{product.id_product} added to cache')
        return self.repository.add(product) 
    
    def delete_product(self, id_product: int) -> None:  
        product = self.repository.find_by_id(id_product)
        if product:
            product.active = False
            cache.delete(f'product_{id_product}')
            logging.info(f'product_{product.id_product} deleted to cache')
            self.repository.update(product)
            return None
        
        logging.error("Unknown product to delete")
        return product 

    def update_product(self, id_product: int, args: dict) -> Product:  
        product = self.repository.find_by_id(id_product)
        if product:
            for key, value in args.items():
                setattr(product, key, value) if hasattr(product, key) else logging.warning("Unknown attr in add_prod")
            
            cache.set(f'product_{id_product}', product, timeout=60)
            logging.info(f'product_{product.id_product} added to cache')
            return self.repository.update(product)
        
        logging.error("Unknown product to update")
        return product
    
    def get_product_by_id(self, id_product: int) -> Product:
        product = cache.get(f'product_{id_product}')
        if product is None:
            product = self.repository.find_by_id(id_product)
            cache.set(f'product_{id_product}', product, timeout=60)
            logging.info(f'product_{product.id_product} added to cache')

        logging.info(f'product_{product.id_product} retrieved to cache')    
        return product
    
    def get_all_active(self) -> list[Product]:
        product = cache.get('active_products_list')
        if product is None:
            product = self.repository.get_all_active()
            cache.set('active_products_list', product, timeout=60)
            logging.info('All active products found has been added to cache successfully')

        logging.info('All active products found successfully from cache')    
        return product
    
    def get_all(self) -> list[Product]:
        product = cache.get('products_list_w_d')
        if product is None:
            product = self.repository.get_all()
            cache.set('products_list_w_d', product, timeout=60)
            logging.info('All products found has been added to cache successfully')

        logging.info('All products found successfully from cache')
        return product
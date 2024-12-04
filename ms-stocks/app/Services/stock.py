from app import cache
from app.Models.stock import Stock
from app.Repositories.stock import StockRepository
from .format_logs import format_logs
from dataclasses import dataclass

logging = format_logs('StockServices')

@dataclass
class StockServices():
    repository = StockRepository()

    def add_stock(self, args: dict) -> Stock:
        stock = Stock()
        for key, value in args.items():
            setattr(stock, key, value) if hasattr(stock, key) else logging.warning("Unknown attr in add_stock")

        cache.set(f'stock_{stock.id_stock}', stock, timeout=60)
        logging.info(f'Stock_{stock.id_stock} added to cache')  
        return self.repository.add_stock(stock)

    def update_stock(self, id_stock:int, args:dict) -> Stock:
        stock = self.repository.find_by_id(id_stock)
        if stock:
            for key, value in args.items():
                setattr(stock, key, value) if hasattr(stock, key) else logging.warning("Unknown attr in add_stock")
                
            cache.set(f'stock_{id_stock}', stock, timeout=60)
            logging.info(f'stock_{stock.id_stock} added to cache')
            return self.repository.update_stock(stock)
        logging.error("Unknown stock to update")
        return stock

    def delete_stock(self, id_stock: int) -> None:
        stock = self.repository.find_by_id(id_stock)
        if stock:
            stock.active = False
            cache.delete(f'stock_{id_stock}')
            logging.info(f'stock_{stock.id_stock} deleted to cache')
            self.repository.update_stock(stock)
            return None
            
        logging.error("Unknown stock to delete")
        return stock

    def find_by_id(self, id_stock: int) -> Stock:
        stock = cache.get(f'stock_{id_stock}')
        if stock is None:
            stock = self.repository.find_by_id(id_stock)
            cache.set(f'stock_{id_stock}', stock, timeout=60)
            logging.info(f'stock_{stock.id_stock} added to cache')

        logging.info(f'stock_{stock.id_stock} retrieved to cache')    
        return stock
    # El siguiente método traerá el stock que esté relacionado con un product_id
    def find_by_product_id(self, id_product: int) -> Stock:
        stock = cache.get(f'stock_product_id_{id_product}')
        if stock is None:
            stock = self.repository.find_by_product_id(id_product)
            cache.set(f'stock_product_id_{id_product}', stock, timeout=10)
            logging.info(f'stock_product_id_{id_product} added to cache')
        logging.info(f'stock_product_id_{id_product} retrieved to cache')    
        return stock

    # La siguiente función traerá los productos con determinado id que han sido ingresados
    def find_by_id_in(self, id_product: int) -> list[Stock]:
        list_stock = cache.get('in_stock_list')
        if list_stock is None:
            list_stock = self.repository.find_by_id_in(id_product)
            cache.set('in_stock_list', list_stock, timeout=3600)
            logging.info('in_stock_list added to cache')

        logging.info('in_stock_list retrieved to cache')    
        return list_stock
    
    # La siguiente función traerá los productos con determinado id que han sido retirados
    def find_by_id_out(self, id_product: int) -> list[Stock]:
        list_stock = cache.get('out_stock_list')
        if list_stock is None:
            list_stock = self.repository.find_by_id(id_product)
            cache.set('out_stock_list', list_stock, timeout=3600)
            logging.info('out_stock_list added to cache')

        logging.info('out_stock_list retrieved to cache')    
        return list_stock

    def get_all_active(self) -> list[Stock]:
        list_stock = cache.get('active_stocks_list')
        if list_stock is None:
            list_stock = self.repository.get_all_active()
            cache.set('active_stocks_list', list_stock, timeout=3600)
            logging.info('All active stocks found has been added to cache successfully')

        logging.info('All active stocks found successfully from cache')    
        return list_stock

    def get_all(self) -> list[Stock]:
            list_stock = cache.get('stocks_list_w_d')
            if list_stock is None:
                list_stock = self.repository.get_all()
                cache.set('stocks_list_w_d', list_stock, timeout=3600)
                logging.info('All stocks found has been added to cache successfully')

            logging.info('All stocks found successfully from cache')
            return list_stock
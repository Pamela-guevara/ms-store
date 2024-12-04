import os, requests
from dataclasses import dataclass
from app import cache
from app.Services.format_logs import format_logs
from app.Models.stock import Stock
from app.Schemas.stock import stock_schema
from app.Models.cart import Cart
from threading import Lock
from multiprocessing import Lock as work_lock

logging = format_logs('LinkedStockService')
locker = Lock()
worker_locker = work_lock()

@dataclass
class LinkedStocks():
    url = os.getenv('STOCKS_URL')
    stock = Stock()

    # Retira un producto del stock y lo agrega al carrito de compras

    def add_product_to_cart(self, cart: Cart) -> None:
        worker_locker.acquire()
        locker.acquire()
        self.stock.in_out = 2
        self.stock.id_product = cart.product.id_product
        res = requests.get(f'{self.url}/get_by_product/{cart.product.id_product}')
        stocks = stock_schema.loads(res.content)
       
        if res.status_code == 200 and stocks['quantity'] >= cart.quantity:
            self.stock.quantity = stocks['quantity'] - cart.quantity
        else:
            logging.error(f'There is not enough stock for product {cart.product.id_product}')
            raise BaseException(f'There is not enough stock for product {cart.product.id_product}')
        
        body = stock_schema.dumps(self.stock)
        response = requests.put(f"{self.url}/update/{stocks['id_stock']}", json=body)
        data = stock_schema.loads(res.content)
        if response.status_code == 201:
            logging.info(f"Stock: {data['id_stock']}\n{data}")
        else:
            logging.error(f'Error in stock-ms')
            raise BaseException('Error in stock-ms')
        worker_locker.release()
        locker.release()


    # Devuelve el producto al stock y lo retira del carrito de compras

    def return_product_to_stock(self, cart: Cart) -> None:
        if cache.get(f'stock_{self.stock.id_stock}'):
            cache.delete(f'stock_{self.stock.id_stock}')
            
        self.stock.in_out = 1
        self.stock.id_product = cart.product.id_product
        res = requests.get(f'{self.url}/get_by_product/{cart.product.id_product}').json()

        if res:
            self.stock.id_stock = res.id_stock
            self.stock.quantity = res.quantity + cart.quantity
        else:
            logging.error('There is not a stock for product id: {cart.product.id_product}')
            raise BaseException('Error in stock-ms, stock id not found')
        
        body = stock_schema.dump(self.stock)
        response = requests.put(f'{self.url}/update/{self.stock.id_stock}', body).json()

        if response.status_code == 200:
            logging.info(f'Stock: {res.id_stock}\n{res}')
        else:
            logging.error(f'Error in stock-ms compensation')
            raise BaseException('Error in stock-ms compensation')

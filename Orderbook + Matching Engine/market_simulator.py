import random
import pandas as pd
from order_book import OrderBook
import config  # Import config.py

class MarketSimulator:
    def __init__(self, start_price=config.START_PRICE, max_quantity=config.MAX_QUANTITY, volatility=config.VOLATILITY):
        self.start_price = start_price  # Initial price from config
        self.max_quantity = max_quantity  # Maximum order quantity from config
        self.volatility = volatility  # Price fluctuation from config
        self.current_price = start_price  # Mid-price
        self.order_id = 0  # To track order IDs
        self.order_book = OrderBook()  # Initialize the order book

    def generate_order(self):
        # Randomize if it is a bid or ask
        order_type = random.choice(["bid", "ask"])
        
        # Price fluctuation following a normal distribution
        price_fluctuation = random.gauss(0, self.volatility)  # Mean is 0, std dev is volatility
        price = self.current_price + price_fluctuation if order_type == "ask" else self.current_price - price_fluctuation
        
        # Generate a random quantity
        quantity = random.gauss(self.max_quantity)
        
        # Increment order ID
        self.order_id += 1

        # Create the order
        order = {
            "order_id": self.order_id,
            "type": order_type,
            "price": round(price, 2),
            "quantity": round(quantity)
        }

        # Add the order to the order book
        self.order_book.add_order(order)

        return order

    def simulate_order(self):
        """
        Simulate one order at a time and return the updated order book depth, spread, and log.
        """
        self.generate_order()
        bid_depth, ask_depth, spread = self.order_book.get_combined_depth()  # Get combined bid-ask depth and spread
        order_log = self.order_book.get_order_log()  # Get order log

        return bid_depth, ask_depth, spread, order_log  # Return all 4 values
  
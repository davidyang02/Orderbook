import pandas as pd
import time


class OrderBook:
    def __init__(self):
        # Store bids with price as the key and quantity as the value
        self.bids = {}  
        # Store asks with price as the key and quantity as the value
        self.asks = {}  
        # Log to store the order details (price, type, time)
        self.order_log = []  
        # Trade log to store executed trades
        self.trade_log = []

    def add_order(self, order):
        # Record the order with the current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.order_log.append({
            'type': order['type'],
            'price': order['price'],
            'quantity': order['quantity'],
            'time': timestamp
        })

        # Match the order with opposite side orders if possible
        if order['type'] == 'bid':
            self.match_bid(order['price'], order['quantity'])
        elif order['type'] == 'ask':
            self.match_ask(order['price'], order['quantity'])

    def match_bid(self, bid_price, bid_quantity):
        # Try to match bid with existing asks
        while bid_quantity > 0 and self.asks:
            time.sleep(0.0)
            # Find the lowest ask that can match this bid
            lowest_ask_price = min(self.asks.keys())
            if lowest_ask_price > bid_price:
                break  # No match possible, exit loop

            ask_quantity = self.asks[lowest_ask_price]

            if bid_quantity >= ask_quantity:
                # Fully match this ask
                self.execute_trade('bid', lowest_ask_price, ask_quantity)
                bid_quantity -= ask_quantity
                del self.asks[lowest_ask_price]  # Remove fully matched ask
            else:
                # Partially match this ask
                self.execute_trade('bid', lowest_ask_price, bid_quantity)
                self.asks[lowest_ask_price] -= bid_quantity
                bid_quantity = 0  # Fully filled bid

        # If there is remaining bid quantity, add it to the bid book
        if bid_quantity > 0:
            if bid_price in self.bids:
                self.bids[bid_price] += bid_quantity
            else:
                self.bids[bid_price] = bid_quantity

    def match_ask(self, ask_price, ask_quantity):
        # Try to match ask with existing bids
        while ask_quantity > 0 and self.bids:
            time.sleep(0.0)
            # Find the highest bid that can match this ask
            highest_bid_price = max(self.bids.keys())
            if highest_bid_price < ask_price:
                break  # No match possible, exit loop

            bid_quantity = self.bids[highest_bid_price]

            if ask_quantity >= bid_quantity:
                # Fully match this bid
                self.execute_trade('ask', highest_bid_price, bid_quantity)
                ask_quantity -= bid_quantity
                del self.bids[highest_bid_price]  # Remove fully matched bid
            else:
                # Partially match this bid
                self.execute_trade('ask', highest_bid_price, ask_quantity)
                self.bids[highest_bid_price] -= ask_quantity
                ask_quantity = 0  # Fully filled ask

        # If there is remaining ask quantity, add it to the ask book
        if ask_quantity > 0:
            if ask_price in self.asks:
                self.asks[ask_price] += ask_quantity
            else:
                self.asks[ask_price] = ask_quantity

    def execute_trade(self, order_type, price, quantity):
        # Log the executed trade
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.trade_log.append({
            'type': order_type,
            'price': price,
            'quantity': quantity,
            'time': timestamp
        })
        print(f"Trade executed: {quantity} units @ {price} ({order_type})")

    def get_combined_depth(self):
        # Convert the bids and asks dictionaries to DataFrames, keeping both price and quantity
        bid_depth = pd.DataFrame(
            sorted(self.bids.items(), key=lambda x: -x[0]), 
            columns=['Bid Price', 'Bid Quantity']
        )
        ask_depth = pd.DataFrame(
            sorted(self.asks.items(), key=lambda x: x[0]), 
            columns=['Ask Price', 'Ask Quantity']
        )

        # Ensure the first values (for spread calculation) are numeric
        try:
            best_bid = float(bid_depth.iloc[0, 0]) if not bid_depth.empty and bid_depth.iloc[0, 0] != '' else None
            best_ask = float(ask_depth.iloc[0, 0]) if not ask_depth.empty and ask_depth.iloc[0, 0] != '' else None
        except ValueError:
            best_bid, best_ask = None, None

        # Calculate the spread (difference between the lowest ask and highest bid)
        if best_bid is not None and best_ask is not None:
            spread = best_ask - best_bid
        else:
            spread = None

        # Return bids, asks, and the calculated spread
        return bid_depth, ask_depth, spread

    def get_order_log(self):
        # Return the log of orders placed
        return pd.DataFrame(self.order_log)

    def get_trade_log(self):
        # Return the log of executed trades
        return pd.DataFrame(self.trade_log)



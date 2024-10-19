from collections import deque

class OrderBook:
    def __init__(self):
        self.bids = {}  # Price -> deque of quantities (FIFO queue)
        self.asks = {}  # Price -> deque of quantities (FIFO queue)

    def add_order(self, order_type, price, quantity):
        if order_type == 'bid':
            self.add_bid(price, quantity)
        elif order_type == 'ask':
            self.add_ask(price, quantity)

    def add_bid(self, price, quantity):
        # Check if a matching ask is available
        if not self.match_ask(price, quantity):
            # No match found, add to bid book
            if price not in self.bids:
                self.bids[price] = deque()  # Use a deque (queue) for FIFO
            self.bids[price].append(quantity)

    def add_ask(self, price, quantity):
        # Check if a matching bid is available
        if not self.match_bid(price, quantity):
            # No match found, add to ask book
            if price not in self.asks:
                self.asks[price] = deque()  # Use a deque (queue) for FIFO
            self.asks[price].append(quantity)

    def match_bid(self, ask_price, ask_quantity):
        matched = False
        # Match with the highest bid available (price >= ask_price)
        for bid_price in sorted(self.bids.keys(), reverse=True):
            if bid_price >= ask_price:
                while self.bids[bid_price] and ask_quantity > 0:
                    bid_quantity = self.bids[bid_price][0]  # FIFO: first bid
                    if bid_quantity <= ask_quantity:
                        print(f"Trade: {bid_quantity} @ {bid_price}")
                        ask_quantity -= bid_quantity
                        self.bids[bid_price].popleft()  # Remove matched bid
                    else:
                        print(f"Trade: {ask_quantity} @ {bid_price}")
                        self.bids[bid_price][0] -= ask_quantity
                        ask_quantity = 0
                if not self.bids[bid_price]:
                    del self.bids[bid_price]  # Remove empty price level
                matched = True
        return matched

    def match_ask(self, bid_price, bid_quantity):
        matched = False
        # Match with the lowest ask available (price <= bid_price)
        for ask_price in sorted(self.asks.keys()):
            if ask_price <= bid_price:
                while self.asks[ask_price] and bid_quantity > 0:
                    ask_quantity = self.asks[ask_price][0]  # FIFO: first ask
                    if ask_quantity <= bid_quantity:
                        print(f"Trade: {ask_quantity} @ {ask_price}")
                        bid_quantity -= ask_quantity
                        self.asks[ask_price].popleft()  # Remove matched ask
                    else:
                        print(f"Trade: {bid_quantity} @ {ask_price}")
                        self.asks[ask_price][0] -= bid_quantity
                        bid_quantity = 0
                if not self.asks[ask_price]:
                    del self.asks[ask_price]  # Remove empty price level
                matched = True
        return matched

# Example usage
order_book = OrderBook()

# Add some bids and asks
order_book.add_order('bid', 100.5, 10)
order_book.add_order('ask', 100.5, 5)
order_book.add_order('ask', 101.0, 10)
order_book.add_order('bid', 100.0, 20)

# Matching will be handled automatically

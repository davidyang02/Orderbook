from order_book import OrderBook

class ManualOrderInput:
    def __init__(self, order_book):
        self.order_book = order_book

    def add_manual_order(self):
        # Prompt the user for order details
        order_type = input("Enter order type (bid/ask): ").strip().lower()
        if order_type not in ['bid', 'ask']:
            print("Invalid order type. Please enter 'bid' or 'ask'.")
            return

        try:
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input. Price must be a number and quantity must be an integer.")
            return

        # Create the order dictionary
        order = {
            'type': order_type,
            'price': price,
            'quantity': quantity
        }

        # Add the order to the order book
        self.order_book.add_order(order)
        print(f"{order_type.capitalize()} order added: {quantity} units at ${price}")

    def manual_input_loop(self):
        # Continuously prompt the user to add orders
        while True:
            add_more = input("Would you like to add a new order? (yes/no): ").strip().lower()
            if add_more == 'yes':
                self.add_manual_order()
            elif add_more == 'no':
                print("Manual input session ended.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

# Usage

# Initialize the order book
order_book = OrderBook()

# Create an instance of the manual input class
manual_input = ManualOrderInput(order_book)

# Start the manual input loop
manual_input.manual_input_loop()

# Display the order log and order book depth
print("\nOrder Log:")
print(order_book.get_order_log())

print("\nOrder Book Depth:")
bid_depth, ask_depth, spread = order_book.get_combined_depth()
print("Bid Depth:\n", bid_depth)
print("Ask Depth:\n", ask_depth)
if spread is not None:
    print(f"\nSpread: {spread}")
else:
    print("\nSpread: Not available (insufficient data)")

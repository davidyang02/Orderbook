import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def setup_figure():
    # Set up the figure with three axes: asks, spread, and bids
    fig, (ax_asks, ax_spread, ax_bids) = plt.subplots(3, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [5, 0.5, 5]})

    # Hide the axes
    ax_bids.xaxis.set_visible(False)
    ax_bids.yaxis.set_visible(False)
    ax_spread.xaxis.set_visible(False)
    ax_spread.yaxis.set_visible(False)
    ax_asks.xaxis.set_visible(False)
    ax_asks.yaxis.set_visible(False)

    # Set background to black
    fig.patch.set_facecolor('black')
    ax_bids.set_facecolor('black')
    ax_spread.set_facecolor('black')
    ax_asks.set_facecolor('black')

    return fig, ax_bids, ax_spread, ax_asks

def customize_table_colors(table, is_bid=True):
    # Set the background color of the table to black
    for key, cell in table.get_celld().items():
        cell.set_facecolor('black')
        cell.set_edgecolor('white')  # Optional: white edges for table cells

    # Customize text colors: green for bids, red for asks
    if is_bid:
        for (row, col), cell in table.get_celld().items():
            cell.set_text_props(color='green')
    else:
        for (row, col), cell in table.get_celld().items():
            cell.set_text_props(color='red')

def update_table(ax_bids, ax_spread, ax_asks, bid_df, ask_df, spread):
    # Clear the existing tables
    ax_bids.clear()
    ax_spread.clear()
    ax_asks.clear()

    # Hide the axes
    ax_bids.xaxis.set_visible(False)
    ax_bids.yaxis.set_visible(False)
    ax_spread.xaxis.set_visible(False)
    ax_spread.yaxis.set_visible(False)
    ax_asks.xaxis.set_visible(False)
    ax_asks.yaxis.set_visible(False)

    # Set background color for axes
    ax_bids.set_facecolor('black')
    ax_spread.set_facecolor('black')
    ax_asks.set_facecolor('black')

    # Update asks table (asks are at the top now)
    if not ask_df.empty:
        ask_df = ask_df.sort_values(by='Ask Price', ascending=False)
        ask_table = ax_asks.table(cellText=ask_df.values, colLabels=ask_df.columns, cellLoc="center", loc="center")
        customize_table_colors(ask_table, is_bid=False)
        ask_table.scale(1, 1.5)  # Scale the table to fit
    else:
        ax_asks.text(0.5, 0.5, 'No Asks', horizontalalignment='center', verticalalignment='center', transform=ax_asks.transAxes, color='white')

    # Show spread in the middle (with reduced space)
    if spread is not None:
        ax_spread.text(0.5, 0.5, f'Spread: {spread:.2f}', horizontalalignment='center', verticalalignment='center', transform=ax_spread.transAxes, color='yellow', fontsize=12)
    else:
        ax_spread.text(0.5, 0.5, 'No Spread Available', horizontalalignment='center', verticalalignment='center', transform=ax_spread.transAxes, color='yellow')

    # Update bids table (bids are now at the bottom)
    if not bid_df.empty:
        bid_table = ax_bids.table(cellText=bid_df.values, colLabels=bid_df.columns, cellLoc="center", loc="center")
        customize_table_colors(bid_table, is_bid=True)
        bid_table.scale(1, 1.5)  # Scale the table to fit
    else:
        ax_bids.text(0.5, 0.5, 'No Bids', horizontalalignment='center', verticalalignment='center', transform=ax_bids.transAxes, color='white')

def animate_table(fig, ax_bids, ax_spread, ax_asks, simulator):
    def update(frame):
        # Generate a new order and get the updated DataFrames
        bid_df, ask_df, spread, _ = simulator.simulate_order()  # Order log removed from the main window
        update_table(ax_bids, ax_spread, ax_asks, bid_df, ask_df, spread)

    # Create an animation that updates every second (1000 ms)
    ani = FuncAnimation(fig, update, frames=range(100), interval=100, repeat=False)

    return ani

def show_plot():
    plt.show()

# Function to show the order log in a separate window
def show_order_log(order_log_df):
    if not order_log_df.empty:
        fig_order_log, ax_order_log = plt.subplots(figsize=(8, 4))
        fig_order_log.patch.set_facecolor('black')
        ax_order_log.set_facecolor('black')
        ax_order_log.xaxis.set_visible(False)
        ax_order_log.yaxis.set_visible(False)

        order_log_table = ax_order_log.table(cellText=order_log_df.values, colLabels=order_log_df.columns, cellLoc="center", loc="center")
        for (row, col), cell in order_log_table.get_celld().items():
            cell.set_fontsize(12)  # Increase font size
            cell.set_facecolor('black')
            cell.set_text_props(color='white')
        order_log_table.scale(1, 1.5)

        plt.show()






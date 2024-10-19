from market_simulator import MarketSimulator
from visualization import setup_figure, animate_table, show_plot

# Create the simulator instance using parameters from the config file
simulator = MarketSimulator()

# Set up the figure and axes for plotting
fig, ax_bids, ax_spread, ax_asks = setup_figure()

# Start the animation
ani = animate_table(fig, ax_bids, ax_spread, ax_asks, simulator)

# Show the live table
show_plot()

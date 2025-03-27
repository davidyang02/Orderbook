# Order Book Engine  

## Overview  
This **Order Book Engine** is a high-performance trading system that simulates a **limit order book**, matching buy and sell orders efficiently. It supports **market and limit orders**, tracks order execution, and provides real-time updates on bid-ask spreads, trade history, and market depth.  

## Features  
- **Limit Order Book (LOB)**: Manages bid and ask orders with price-time priority.  
- **Order Matching Engine**: Executes trades by matching buy and sell orders.  
- **Market & Limit Orders**: Supports instant market orders and queued limit orders.  
- **Trade Execution & Logs**: Records filled trades and order history.  
- **Live Order Book Visualization**: Displays bid-ask spreads and order depth.  
- **Performance Optimization**: Efficient data structures for high-speed processing.  

## Installation  
Ensure you have Python installed and install the required dependencies:  

```bash
pip install pandas numpy matplotlib plotly dash
```

## Model & Visualizations  
- **Order Matching Engine**: Implements price-time priority matching.  
- **Trade Execution Log**: Stores completed trades with timestamps.  
- **Live Order Book Depth Chart**: Visualizes bid and ask distribution.  
- **Trade Price & Volume Analysis**: Displays market activity over time.  

## Example Output  
- **Order Book Snapshot**: Displays open buy/sell orders.  
- **Trade Execution Log**: Shows matched trades.  
- **Order Book Depth Chart**: Visualizes market liquidity.  



## License  
This project is open-source and available under the **MIT License**.  

# backtest.py
# Placeholder script for historical backtesting

import pandas as pd

def run_backtest(positions, historical_prices):
    """
    Compute simple P&L based on historical prices.
    """
    pnl = pd.DataFrame(index=historical_prices.index)
    for symbol in positions['Symbol']:
        if symbol in historical_prices.columns:
            pnl[symbol] = (historical_prices[symbol] - positions.loc[positions['Symbol']==symbol,'Avg_Price'].values[0]) * positions.loc[positions['Symbol']==symbol,'Quantity'].values[0]
    pnl['Total'] = pnl.sum(axis=1)
    return pnl

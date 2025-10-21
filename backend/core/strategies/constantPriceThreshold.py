from typing import Dict, List

from pandas import DataFrame
from core.portfolio import Portfolio
from core.strategies.base import Strategy
from core.tradeRequest import TradeRequest


class ConstantPriceThresholdStrategy(Strategy):
    def __init__(self, threshold: float, daysToClose: int, quantity: int):
        """
        Initializes the Constant Price Threshold strategy.

        Parameters:
            threshold (float): The price level that triggers a buy signal.
            daysToClose (int): The number of days to hold a position before selling.
            quantity (int): The number of shares to trade in each transaction.
        """
        super().__init__()
        self.threshold = threshold
        self.daysToClose = daysToClose
        self.quantity = quantity
        self.positions = {}

    def next(self, marketData: DataFrame, portfolio: Portfolio) -> List[TradeRequest]:
        """
        Generates trade requests based on the latest market data.

        Parameters:
            marketData (DataFrame): A DataFrame containing market data up to the
            current time step, with a (Date, Symbol) MultiIndex.
            portfolio (Portfolio): The current portfolio object (not used in this strategy).

        Returns:
            trades (List[TradeRequest]): A list of buy or sell orders to be executed.
        """
        trades = []
        for symbol in marketData.index.get_level_values("Symbol").unique():
            symbolData = marketData.xs(symbol, level="Symbol")
            # Continue, if its the first day
            if len(symbolData) < 2:
                continue
            latestPrice = symbolData.iloc[-1]["Close"]
            previousPrice = symbolData.iloc[-2]["Close"]
            # Price must strike from below the threshold
            if latestPrice >= self.threshold and previousPrice <= latestPrice and previousPrice <= self.threshold:
                trades.append(TradeRequest(symbol, self.quantity, "BUY"))
                if symbol not in self.positions:
                    self.positions[symbol] = [len(symbolData)]
                else:
                    self.positions[symbol].append(len(symbolData))

            # Sell positions after daysToClose
            if symbol in self.positions:
                for time in self.positions[symbol]:
                    if len(symbolData) - time >= self.daysToClose:
                         trades.append(TradeRequest(symbol, self.quantity, "SELL"))
        return trades

    def onStart(self):
        """
        A callback method executed once at the start of a backtest.
        """
        pass

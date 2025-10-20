from typing import Dict, List

from pandas import DataFrame
from core.portfolio import Portfolio
from core.strategies.base import Strategy
from core.tradeRequest import TradeRequest


class ConstantPriceThresholdStrategy(Strategy):
    def __init__(self, threshold: float, daysToClose: int, quantity: int):
        super().__init__()
        self.threshold = threshold
        self.daysToClose = daysToClose
        self.quantity = quantity
        self.positions = {}

    def next(self, marketData: DataFrame, portfolio: Portfolio) -> List[TradeRequest]:
        trades = []
        for symbol in marketData.index.get_level_values("Symbol").unique():
            symbolData = marketData.xs(symbol, level="Symbol")
            if len(symbolData) < 2:
                continue
            latestPrice = symbolData.iloc[-1]["Close"]
            previousPrice = symbolData.iloc[-2]["Close"]
            if latestPrice >= self.threshold and previousPrice <= latestPrice and previousPrice <= self.threshold:
                trades.append(TradeRequest(symbol, self.quantity, "BUY"))
                if symbol not in self.positions:
                    self.positions[symbol] = [len(symbolData)]
                else:
                    self.positions[symbol].append(len(symbolData))

            if symbol in self.positions:
                for time in self.positions[symbol]:
                    if len(symbolData) - time >= self.daysToClose:
                         trades.append(TradeRequest(symbol, self.quantity, "SELL"))
        return trades

    def onStart(self):
        pass

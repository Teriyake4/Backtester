from typing import Dict, List

from pandas import DataFrame
from backend.core.portfolio import Portfolio
from backend.core.strategies.base import Strategy
from backend.core.tradeRequest import TradeRequest


class ConstantPriceThresholdStrategy(Strategy):
    def __init__(self, threshold: float, daysToClose: int, quantity: int):
        super().__init__()
        self.threshold = threshold
        self.daysToClose = daysToClose
        self.quantity = quantity

    def next(self, marketData: DataFrame, portfolio: Portfolio) -> List[TradeRequest]:
        trades = []
        for symbol in marketData.index.get_level_values("Symbol").unique():
            latestPrice = marketData.xs(symbol, level="Symbol").iloc[-1]["Close"]
            previousPrice = marketData.xs(symbol, level="Symbol").iloc[-1]["Close"]
            if latestPrice >= self.threshold and previousPrice < latestPrice:
                trades.append(TradeRequest(symbol, self.quantity, "BUY"))
        return trades

    def onStart(self):
        pass

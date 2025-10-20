from datetime import datetime

from core.tradeRequest import Side


class Trade:
    def __init__(self, symbol: str, shares: int, side: Side, sharePrice: float, timestamp: datetime):
        self.symbol = symbol
        self.shares = shares
        self.side = side
        self.sharePrice = sharePrice
        self.timestamp = timestamp
    
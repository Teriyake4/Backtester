from typing import Literal


Side = Literal["BUY", "SELL"]

class TradeRequest:
    def __init__(self, symbol: str, shares: int, side: Side):
        self.symbol = symbol
        self.shares = shares
        self.side = side
        
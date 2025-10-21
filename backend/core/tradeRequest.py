from typing import Literal


Side = Literal["BUY", "SELL"]

class TradeRequest:
    def __init__(self, symbol: str, shares: int, side: Side):
        """
        Initializes a TradeRequest object, representing an intent to place a trade.

        Parameters:
            symbol (str): The asset symbol for the requested trade.
            shares (int): The number of shares to be traded.
            side (Side): The side of the requested trade, BUY or SELL.
        """
        self.symbol = symbol
        self.shares = shares
        self.side = side
        
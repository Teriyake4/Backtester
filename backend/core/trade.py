from datetime import datetime

from core.tradeRequest import Side


class Trade:
    def __init__(self, symbol: str, shares: int, side: Side, sharePrice: float, timestamp: datetime):
        """
        Initializes a Trade object, representing a completed transaction.

        Parameters:
            symbol (str): The asset symbol that was traded.
            shares (int): The number of shares transacted.
            side (Side): The side of the trade BUY or SELL.
            sharePrice (float): The price per share at which the trade executed.
            timestamp (datetime): The date and time the trade was executed.
        """
        self.symbol = symbol
        self.shares = shares
        self.side = side
        self.sharePrice = sharePrice
        self.timestamp = timestamp
    
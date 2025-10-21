from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pandas import DataFrame

from core.portfolio import Portfolio
from core.tradeRequest import TradeRequest


class Strategy(ABC):
    def __init__(self) -> None:
        """
        Initializes the strategy.
        """
        pass
    
    @abstractmethod
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
        pass

    @abstractmethod
    def onStart(self):
        """
        A callback method executed once at the start of a backtest.
        """
        pass
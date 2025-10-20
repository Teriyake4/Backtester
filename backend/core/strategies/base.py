from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pandas import DataFrame

from backend.core.portfolio import Portfolio
from backend.core.tradeRequest import TradeRequest


class Strategy(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def next(self, marketData: DataFrame, portfolio: Portfolio) -> List[TradeRequest]:
        pass

    @abstractmethod
    def onStart(self):
        pass
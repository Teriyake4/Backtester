from abc import ABC, abstractmethod
from datetime import datetime

from pandas import DataFrame


class DBInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getData(self, symbol: str, date: datetime) -> DataFrame:
        pass

    @abstractmethod
    def getDataRange(self, symbol: str, startDate: datetime, endDate: datetime) -> DataFrame:
        pass

    @abstractmethod
    def setData(self, symbol: str, data: DataFrame) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

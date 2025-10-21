from abc import ABC, abstractmethod
from datetime import datetime

from pandas import DataFrame


class DBInterface(ABC):
    def __init__(self):
        """
        Initializes the database.
        """
        pass

    @abstractmethod
    def getData(self, symbol: str, date: datetime) -> DataFrame:
        """
        Retrieves market data for a single symbol on a specific date.

        Parameters:
            symbol (str): The asset symbol to query.
            date (datetime): The specific date for which to retrieve data.

        Returns:
            data (DataFrame): A pandas DataFrame containing the data for the specified symbol and date, indexed by "Date".
        """
        pass

    @abstractmethod
    def getDataRange(self, symbol: str, startDate: datetime, endDate: datetime) -> DataFrame:
        """
        Retrieves market data for a single symbol over a specified date range.

        Parameters:
            symbol (str): The asset symbol to query.
            startDate (datetime): The start date for the data range, inclusive.
            endDate (datetime): The end date for the data range, inclusive.

        Returns:
            data (DataFrame): A pandas DataFrame containing the data for the
            symbol within the date range, sorted chronologically
            and indexed by "Date".
        """
        pass

    @abstractmethod
    def setData(self, symbol: str, data: DataFrame) -> None:
        """
        Inserts or replaces market data for a symbol from a pandas DataFrame.

        Parameters:
            symbol (str): The asset symbol for which data is being inserted.
            data (DataFrame): A pandas DataFrame containing OHLCV data. It must
            have a datetime index.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        pass

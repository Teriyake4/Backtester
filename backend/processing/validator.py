from datetime import datetime, timedelta

from pandas import DataFrame
from pandas.tseries.holiday import USFederalHolidayCalendar
import pandas as pd

from database import sqLiteDB
from database.base import DBInterface
from processing.ingester import addSymbol


class Validator:
    def getDataRange(symbol: str, startDate: datetime, endDate: datetime, database: DBInterface) -> DataFrame:
        """
        Validates and retrieves a complete range of market data for a symbol.

        It checks for missing business days and automatically
        fetches and backfills any gaps it finds and updates the database.

        Parameters:
            symbol (str): The asset symbol to query.
            startDate (datetime): The start date for the data range, inclusive.
            endDate (datetime): The end date for the data range, inclusive.
            database (DBInterface): A database connection object used for data retrieval and storage.

        Returns:
            data (DataFrame): A pandas DataFrame containing a complete and sorted set of market data for the 
            specified range.
        """
        data = database.getDataRange(symbol, startDate, endDate)

        if data.empty:
            addSymbol(symbol, startDate, endDate, database)
            data = database.getDataRange(symbol, startDate, endDate)
            return data


        expectedDates = pd.bdate_range(start=startDate, end=endDate)
        holidays = USFederalHolidayCalendar().holidays(start=startDate, end=endDate)
        expectedDates.difference(holidays)

        consecutiveStartDate = None
        for date in expectedDates:
            # if date is not in data
            # if values at a certain date are null
            if date not in data.index or data.loc[date].isnull().any():
                if consecutiveStartDate is None:
                    consecutiveStartDate = date
                    consecutiveStartDate = consecutiveStartDate.tz_localize(None)
            # If there is filled date on current date and previous data that was missing
            # then fetch the previous data
            elif consecutiveStartDate:
                end = date - timedelta(1)
                addSymbol(symbol, consecutiveStartDate, end, database)
                data.loc[consecutiveStartDate : end] = database.getDataRange(symbol, consecutiveStartDate, end)
                consecutiveStartDate = None

        if consecutiveStartDate:
            # Remove timezone from dates
            expectedDate = expectedDates[-1]
            expectedDate = expectedDate.tz_localize(None)
            addSymbol(symbol, consecutiveStartDate, expectedDate, database)
            data.loc[consecutiveStartDate : expectedDate] = database.getDataRange(symbol, consecutiveStartDate, expectedDate)

        data.sort_index()

        return data
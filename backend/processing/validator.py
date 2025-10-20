from datetime import datetime, timedelta

from pandas import DataFrame
from pandas.tseries.holiday import USFederalHolidayCalendar
import pandas as pd

from database import sqLiteDB
from database.base import DBInterface
from processing.ingester import addSymbol


class Validator:

    def getDataRange(symbol: str, startDate: datetime, endDate: datetime, database: DBInterface) -> DataFrame:
        data = database.getDataRange(symbol, startDate, endDate)

        if data.empty:
            addSymbol(symbol, startDate, endDate, database)
            data = database.getDataRange(symbol, startDate, endDate)
            return data


        expectedDates = pd.bdate_range(start=startDate, end=endDate)
        holidays = USFederalHolidayCalendar().holidays(start=startDate, end=endDate)
        expectedDates.difference(holidays)

        # actualDates = data.index.normalize()
        # missingDates = expectedDates.difference(actualDates)
        consecutiveStartDate = None
        for date in expectedDates:
            # if date is not in data
            # if values at a certain date are null
            if date not in data.index or data.loc[date].isnull().any():
                if consecutiveStartDate is None:
                    consecutiveStartDate = date
            # If there is filled date on current date and previous data that was missing
            # then fetch the previous data
            elif consecutiveStartDate:
                end = date - timedelta(1)
                addSymbol(symbol, consecutiveStartDate, end, database)
                data.loc[consecutiveStartDate : end] = database.getDataRange(symbol, consecutiveStartDate, end)
                consecutiveStartDate = None

        if consecutiveStartDate:
            addSymbol(symbol, consecutiveStartDate, expectedDates[-1], database)
            data.loc[consecutiveStartDate : expectedDates[-1]] = database.getDataRange(symbol, consecutiveStartDate, expectedDates[-1])

        data.sort_index()

        return data
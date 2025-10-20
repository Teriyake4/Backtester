from datetime import datetime, timedelta

from pandas import DataFrame
from pandas.tseries.holiday import USFederalHolidayCalendar
import pandas as pd

from backend.database import sqLiteDB
from backend.database.base import DBInterface
from backend.processing.ingester import addSymbol


class Validator:
    def __init__(self):
        pass

    def getDataRange(symbol: str, startDate: datetime, endDate: datetime, database: DBInterface) -> DataFrame:
        data = database.getDataRange(symbol, startDate, endDate)

        expectedDates = pd.bdate_range(start=startDate, end=endDate)
        holidays = USFederalHolidayCalendar().holidays(start=startDate, end=endDate)
        expectedDates.difference(holidays)

        # actualDates = data.index.normalize()
        # missingDates = expectedDates.difference(actualDates)
        for date in expectedDates:
            # if date is not in data
            # if values at a certain date are null
            if date not in data.index or DataFrame.loc[date].isnull().any():
                addSymbol(symbol, date, date, database)
                data.loc(date) = database.getDate(symbol, date, date)

        data.sort_index()

        return data
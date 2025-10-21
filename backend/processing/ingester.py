from datetime import datetime, timedelta
import os

import yfinance as yf

from database import sqLiteDB
from database.base import DBInterface



def addSymbol(symbol: str, startDate: datetime, endDate: datetime, database: DBInterface) -> None:
    """
    Get historical data for a specified symbol within a date range from Yahoo Finance and put it into the database.

    Parameters:
        symbol (str): Stock symbol to get historical data from.
        startDate (datetime): Start date for the data range, inclusive.
        endDate (datetime): End date for the data range, inclusive.
        database (DBInterface): Database to put the retrieved data into.
    """
    data = yf.download(symbol, start=startDate, end=endDate+timedelta(days=1), interval="1d")
    # Make into single index df
    data.columns = data.columns.droplevel(1)
    database.setData(symbol, data)

if __name__ == "__main__":
    symbol = "MSFT"
    start = datetime(2024, 10, 18)
    end = datetime(2025, 5, 1)

    dbPath = os.path.abspath(os.path.join("..", "data", "symbol_data.db"))
    database = sqLiteDB(dbPath)
    addSymbol(symbol, start, end, database)
    database.close()
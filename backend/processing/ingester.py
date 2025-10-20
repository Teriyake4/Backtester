from datetime import datetime, timedelta

import yfinance as yf

from backend.database import sqLiteDB
from backend.database.base import DBInterface



def addSymbol(symbol: str, startDate: datetime, endDate: datetime, database: DBInterface) -> None:
    """
    Get historical data for a specified symbol within a date range from Yahoo Finance and put it into the database.
    
    Parameters:
        symbol (str): Stock symbol to get historical data from
        startDate (datetime): Start date for the data range, inclusive
        endDate (datetime): End date for the data range, inclusive
        database (DBInterface): Database to put the retrieved data into
    """
    data = yf.download(symbol, start=startDate, end=endDate+timedelta(days=1))
    database.setData(symbol, data)

if __name__ == "__main__":
    symbol = "MSFT"
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    database = sqLiteDB("data/symbol_data.db")
    addSymbol(symbol, start, end, database)
    database.close()
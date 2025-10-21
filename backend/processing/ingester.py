import argparse
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
    parser = argparse.ArgumentParser()

    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--start", type=str, required=True)
    parser.add_argument("--end", type=str, required=True,)

    args = parser.parse_args()

    try:
        startDate = datetime.strptime(args.start, "%Y-%m-%d")
        endDate = datetime.strptime(args.end, "%Y-%m-%d")
    except ValueError:
        print("Error: Use YYYY-MM-DD.")
        exit(1)

    dbPath = os.path.abspath(os.path.join("..", "data", "symbol_data.db"))

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(dbPath), exist_ok=True)
    database = sqLiteDB(dbPath)
    addSymbol(args.symbol, startDate, endDate, database)
    database.close()

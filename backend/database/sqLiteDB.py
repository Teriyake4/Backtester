from datetime import datetime
import sqlite3

from pandas import DataFrame
import pandas as pd


class SQLiteDB():
    def __init__(self, dbPath: str):
        self.con = sqlite3.connect(dbPath)
        self._createTable()

    def _createTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS symbol_data (
            symbol TEXT NOT NULL, 
            date TEXT NOT NULL, 
            open REAL, 
            high REAL, 
            low REAL, 
            close REAL, 
            adjusted_close REAL, 
            volume INTEGER, 
            PRIMARY KEY (symbol, date)
        );
        """
        with self.con:
            self.con.execute(query)

    def getData(self, symbol: str, date: datetime) -> DataFrame:
        dateString = date.strftime("%Y-%m-$d")
        query = "SELECT * FROM symbol_data WHERE symbol = ? AND date = ?"
        data = pd.read_sql_query(query, self.con, params=(symbol, dateString))
        data.rename(
            index={"date": "Date"},
            columns={
                "open" : "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "adjusted_close": "Adj Close",
                "volume": "Volume"
            },
            inplace=True
        )
        data["Date"] = pd.to_datetime(data["Date"])
        return data

    def getDataRange(self, symbol: str, startDate: datetime, endDate: datetime) -> DataFrame:
        startDateString = startDate.strftime("%Y-%m-$d")
        endDateString = endDate.strftime("%Y-%m-$d")
        query = """
        SELECT * FROM symbol_data 
        WHERE symbol = ? AND date BETWEEN ? AND ? 
        ORDER BY date ASC
        """
        data = pd.read_sql_query(query, self.con, params=(symbol, startDateString, endDateString))
        data.rename(
            index={
                "date": "Date",
                "symbol": "Symbol"
            },
            columns={
                "open" : "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "adjusted_close": "Adj Close",
                "volume": "Volume"
            },
            inplace=True
        )
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.set_index(["Date", "Symbol"])
        return data

    def setData(self, symbol: str, data: DataFrame):
        data = data.copy()
        data["symbol"] = symbol
        data.rename(
            index={"Date": "date"},
            columns={
                "Open" : "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adjusted_close",
                "Volume": "volume"
            },
            inplace=True
        )
        data["date"] = data["date"].dt.strftime("%Y-%m-%d")

        columns = [
            "symbol",
            "date",
            "open",
            "high",
            "low",
            "close",
            "adjusted_close",
            "volume"
        ]
        records = data[columns].to_records(index=False).tolist()
        query = """
        INSERT OR REPLACE INTO symbol_data (symbol, date, open, high, low, close, adjusted_close, volume) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.con:
            self.con.executemany(query, records)


    def close(self):
        if self.con:
            self.con.close()
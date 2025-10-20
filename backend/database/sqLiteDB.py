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
        dateString = date.strftime("%Y-%m-%d")
        query = "SELECT * FROM symbol_data WHERE symbol = ? AND date = ?"
        data = pd.read_sql_query(query, self.con, params=(symbol, dateString))
        data.rename(
            columns={
                "date": "Date",
                "symbol": "Symbol",
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
        data = data.set_index("Date")
        return data

    def getDataRange(self, symbol: str, startDate: datetime, endDate: datetime) -> DataFrame:
        startDateString = startDate.strftime("%Y-%m-%d")
        endDateString = endDate.strftime("%Y-%m-%d")
        query = """
        SELECT * FROM symbol_data 
        WHERE symbol = ? AND date BETWEEN ? AND ? 
        ORDER BY date ASC
        """
        data = pd.read_sql_query(query, self.con, params=(symbol, startDateString, endDateString))
        data.rename(
            columns={
                "date": "Date",
                "symbol": "Symbol",
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
        data = data.set_index("Date")
        return data

    def setData(self, symbol: str, data: DataFrame):
        data = data.copy()
        data.reset_index(inplace=True)
        data["Symbol"] = symbol
        if "Adj Close" not in data.columns:
            data["Adj Close"] = data["Close"]
        data.rename(
            columns={
                "Date": "date",
                "Symbol": "symbol",
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
            self.con.commit()


    def close(self):
        if self.con:
            self.con.close()
from datetime import datetime
import os
from typing import Any, Dict, List, Type
import pandas as pd
from core.metrics import Metrics
from core.portfolio import Portfolio
from core.strategies.base import Strategy
from database.sqLiteDB import SQLiteDB
from processing.validator import Validator
from core.backtestRequest import BacktestRequest


class Engine:
    def runBacktest(
            symbols: List[str],
            startDate: datetime,
            endDate: datetime,
            strategyClass: Type[Strategy],
            strategyParams: Dict[str, Any],
            startingCash: float
        ) -> Dict[str, Any]:

        # check db for no missing data
        print("Starting db")
        dbPath = os.path.abspath(os.path.join("..", "data", "symbol_data.db"))
        # os.makedirs(dbPath, exist_ok=True)
        print(dbPath)
        database = SQLiteDB(dbPath)
        startDate = startDate
        endDate = endDate

        print("Getting data")
        # Get data
        listOfData = []
        for symbol in symbols:
            singleData = Validator.getDataRange(symbol, startDate, endDate, database)
            listOfData.append(singleData)

        database.close()
        completeData = pd.concat(listOfData)
        completeData = completeData.set_index("Symbol", append=True).sort_index()

        print("Initiating portfolio and strategy")
        portfolio = Portfolio(startingCash)
        strategy = strategyClass(**strategyParams)
        strategy.onStart()

        print("Backtesting")
        # Main backtest loop
        for date in completeData.index.get_level_values("Date").unique():
            marketData = completeData.loc[:date]

            portfolio._updateValue(marketData)
            trades = strategy.next(marketData, portfolio)
            portfolio._executeTrades(marketData, trades)

        portfolio._liquidate(completeData)

        print("Calculating metrics")
        # Calculate metrics of backtest
        metrics = Metrics(completeData, portfolio)
        results = {
            "profitLoss": metrics.getProfitLoss(),
            "annualizedReturn": metrics.getAnnualizedReturn(),
            "maxDrawdown": metrics.getMaxDrawdown(),
            "winProbability": metrics.getWinProbability(),
            "portfolio": portfolio
        }
        return results

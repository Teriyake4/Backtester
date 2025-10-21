from datetime import datetime
import os
from typing import Any, Dict, List, Type
import pandas as pd
from core.metrics import Metrics
from core.portfolio import Portfolio
from core.strategies.base import Strategy
from database.sqLiteDB import SQLiteDB
from processing.validator import Validator


class Engine:
    def runBacktest(
            symbols: List[str],
            startDate: datetime,
            endDate: datetime,
            strategyClass: Type[Strategy],
            strategyParams: Dict[str, Any],
            startingCash: float
        ) -> Dict[str, Any]:
        """
        Run backtest on a list of symbols within a date range using the specified strategy
        
        Parameters:
            symbols (List[str]): List of symbols to backtest on.
            startDate (datetime): Start date for the data range, inclusive.
            endDate (datetime): End date for the data range, inclusive.
            strategyClass (Strategy): Strategy class to use in the backtest.
            strategyParams (Dict[str, Any]): Dictionary for parameters of strategy class.
            startingCash (float): Initial cash to start backtest with.

        Returns:
            results (Dict[str, Any]): Contains metrics of backtest and portfolio after backtest run.
        """

        # check db for no missing data
        dbPath = os.path.abspath(os.path.join("..", "data", "symbol_data.db"))
        os.makedirs(os.path.dirname(dbPath), exist_ok=True)
        database = SQLiteDB(dbPath)
        startDate = startDate
        endDate = endDate

        # Get data
        listOfData = []
        for symbol in symbols:
            singleData = Validator.getDataRange(symbol, startDate, endDate, database)
            listOfData.append(singleData)

        database.close()
        completeData = pd.concat(listOfData)
        completeData = completeData.set_index("Symbol", append=True).sort_index()

        portfolio = Portfolio(startingCash)
        strategy = strategyClass(**strategyParams)
        strategy.onStart()

        # Main backtest loop
        for date in completeData.index.get_level_values("Date").unique():
            marketData = completeData.loc[:date]

            portfolio._updateValue(marketData)
            trades = strategy.next(marketData, portfolio)
            portfolio._executeTrades(marketData, trades)

        portfolio._liquidate(completeData)

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

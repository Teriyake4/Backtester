from pandas import DataFrame
import pandas as pd
from backend.core.portfolio import Portfolio
from backend.core.strategies.base import Strategy
from backend.database.sqLiteDB import SQLiteDB
from backend.processing.validator import Validator
from backend.interface.backtestRequest import BacktestRequest


class Engine:
    def runBacktest(request: BacktestRequest, strategy: Strategy):
        # check db for no missing data
        database = SQLiteDB("data/symbol_data.sb")
        startDate = request.startDate
        endDate = request.endDate

        # Get data
        listOfData = []
        days = -1
        for symbol in request.symbols:
            singleData = Validator.getDataRange(symbol, startDate, endDate, database)
            singleData["Symbol"] = symbol
            listOfData.append(singleData)
            if days == -1:
                days = singleData.shape[0]

        completeData = pd.concat(listOfData)
        completeData = completeData.set_index("Symbol", append=True).swaplevel("Symbol", 0).sort_index()
        

        strategy.onStart()
        portfolio = Portfolio(request.startingCash)

        # Main backtest loop
        for i in range(days):
            marketData = completeData.iloc[0:i+1]

            portfolio._updateValue(marketData)
            trades = strategy.next(marketData, portfolio)
            portfolio._executeTrades(marketData, trades)

        portfolio._liquidate(marketData)




        database.close()
        

        # if missing, call ingestion script
        # run backtest with strat
        # run metrics with trades
        # return metrics


    # runBacktest(startDate, endDate) -> results

    # setSymbols([symbols])
    
    # setStrategy(strategy, strategyParams)

    # setTester(testingConditions)
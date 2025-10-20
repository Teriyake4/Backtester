from typing import List

from pandas import DataFrame
import pandas as pd

from backend.core.trade import Trade
from backend.core.tradeRequest import TradeRequest


class Portfolio:
    def __init__(self, cash: float):
        self.initialCash = cash
        self.cash = cash
        self.holdings = {} # {symbol: shares}
        self.trades = []
        multiIndex = pd.MultiIndex.from_tuples(names=["Date", "Symbol"])
        self.history = pd.DataFrame(index=multiIndex, columns=["Value"])
        self.cashHistory = pd.DataFrame(columns="Value")

    def getInitialCash(self):
        return self.initialCash
    
    def getCash(self):
        return self.cash
    
    def getHoldings(self):
        return self.holdings
    
    def getTrades(self):
        return self.trades
    
    def getHistory(self):
        return self.history

    def _updateValue(self, marketData: DataFrame):
        date = marketData.index[-1][0]
        self.cashHistory.loc[date] = self.cash
        for symbol, shares in self.holdings.items():
            self.history.loc[(date, symbol)] = shares * marketData.loc[(date, symbol), "Close"]

    def _executeTrades(self, marketData: DataFrame, tradeReqeusts: List[TradeRequest]):
        date = marketData.index[-1][0]
        buyRequests = []
        for request in tradeReqeusts:
            symbol = request.symbol
            if request.side is "BUY": # Execute SELL orders first to free up cash
                buyRequests.append(request)
                continue
            sharePrice = marketData.loc[(date, symbol), "Close"]
            if symbol not in self.holdings:
                continue
            elif request.shares > self.holdings[symbol]:
                continue
            else:
                self.holdings[symbol] -= request.shares
            trade = Trade(
                symbol,
                request.shares,
                request.side,
                sharePrice,
                date
            )
            self.trades.append(trade)
            value = request.shares * sharePrice
            self.cash += value

        # Execute BUY orders
        for request in buyRequests:
            sharePrice = marketData.loc[(date, symbol), "Close"]
            value = request.shares * sharePrice
            if value > self.cash:
                continue
            elif symbol not in self.holdings:
                self.holdings[symbol] = request.shares
            else:
                self.holdings[symbol] += request.shares
            trade = Trade(
                symbol,
                request.shares,
                request.side,
                sharePrice,
                date
            )
            self.trades.append(trade)
            self.cash -= value
                    
    def _liquidate(self, marketData: DataFrame):
        for symbol, shares in self.holdings.items():
            date = marketData.index[-1][0]
            sharePrice = marketData.loc[(date, symbol), "Close"]
            trade = Trade(
                symbol,
                shares,
                "SELL",
                sharePrice,
                date
            )
            self.trades.append(trade)
            value = shares * sharePrice
            self.cash += value


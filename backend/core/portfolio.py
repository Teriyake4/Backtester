from typing import Dict, List

from pandas import DataFrame
import pandas as pd

from core.trade import Trade
from core.tradeRequest import TradeRequest


class Portfolio:
    def __init__(self, cash: float):
        self._initialCash = cash
        self._cash = cash
        self._holdings = {} # {symbol: shares}
        self._trades = []
        multiIndex = pd.MultiIndex.from_tuples([], names=["Date", "Symbol"])
        self._history = pd.DataFrame(index=multiIndex, columns=["Value"])
        self._cashHistory = pd.DataFrame(columns=["Value"])

    def getInitialCash(self) -> float:
        return self._initialCash
    
    def getCash(self) -> float:
        return self._cash
    
    def getHoldings(self) -> Dict[str, int]:
        return self._holdings
    
    def getTrades(self) -> List[Trade]:
        return self._trades
    
    def getHistory(self) -> DataFrame:
        return self._history
    
    def getCashHistory(self) -> DataFrame:
        return self._cashHistory

    def _updateValue(self, marketData: DataFrame):
        date = marketData.index.get_level_values("Date")[-1]
        self._cashHistory.loc[date, "Value"] = self._cash
        for symbol, shares in self._holdings.items():
            self._history.loc[(date, symbol), "Value"] = shares * marketData.loc[(date, symbol), "Close"]

            

    def _executeTrades(self, marketData: DataFrame, tradeReqeusts: List[TradeRequest]):
        date = marketData.index.get_level_values("Date")[-1]
        buyRequests = []
        for request in tradeReqeusts:
            if request.side == "BUY": # Execute SELL orders first to free up cash
                buyRequests.append(request)
                continue
            symbol = request.symbol
            sharePrice = marketData.loc[(date, symbol), "Close"]
            if symbol not in self._holdings:
                continue
            elif request.shares > self._holdings[symbol]:
                continue
            else:
                self._holdings[symbol] -= request.shares
            trade = Trade(
                symbol,
                request.shares,
                request.side,
                sharePrice,
                date
            )
            self._trades.append(trade)
            value = request.shares * sharePrice
            self._cash += value

        # Execute BUY orders
        for request in buyRequests:
            symbol = request.symbol
            sharePrice = marketData.loc[(date, symbol), "Close"]
            value = request.shares * sharePrice
            if value > self._cash:
                continue
            elif symbol not in self._holdings:
                self._holdings[symbol] = request.shares
            else:
                self._holdings[symbol] += request.shares
            trade = Trade(
                symbol,
                request.shares,
                request.side,
                sharePrice,
                date
            )
            self._trades.append(trade)
            self._cash -= value
                    
    def _liquidate(self, marketData: DataFrame):
        for symbol, shares in self._holdings.items():
            if shares == 0:
                continue
            date = marketData.index.get_level_values("Date")[-1]
            sharePrice = marketData.loc[(date, symbol), "Close"]
            trade = Trade(
                symbol,
                shares,
                "SELL",
                sharePrice,
                date
            )
            self._trades.append(trade)
            value = shares * sharePrice
            self._cash += value


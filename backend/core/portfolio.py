from typing import Dict, List

from pandas import DataFrame
import pandas as pd

from core.trade import Trade
from core.tradeRequest import TradeRequest


class Portfolio:
    def __init__(self, cash: float):
        """
        Initializes the portfolio with a starting amount of cash.

        Parameters:
            cash (float): The initial amount of cash to start the portfolio with.
        """
        self._initialCash = cash
        self._cash = cash
        self._holdings = {} # {symbol: shares}
        self._trades = []
        multiIndex = pd.MultiIndex.from_tuples([], names=["Date", "Symbol"])
        self._history = pd.DataFrame(index=multiIndex, columns=["Value"])
        self._cashHistory = pd.DataFrame(columns=["Value"])

    def getInitialCash(self) -> float:
        """
        Retrieves the initial cash the portfolio was funded with.

        Returns:
            initialCash (float): The starting cash amount.
        """
        return self._initialCash
    
    def getCash(self) -> float:
        """
        Retrieves the current available cash in the portfolio.

        Returns:
            cash (float): The current cash balance.
        """
        return self._cash
    
    def getHoldings(self) -> Dict[str, int]:
        """
        Retrieves the current asset holdings of the portfolio.

        Returns:
            holdings (Dict[str, int]): A dictionary mapping each symbol to the
            number of shares held.
        """
        return self._holdings
    
    def getTrades(self) -> List[Trade]:
        """
        Retrieves the history of all executed trades.

        Returns:
            trades (List[Trade]): A list of all Trade objects that have been
            executed by the portfolio.
        """
        return self._trades
    
    def getHistory(self) -> DataFrame:
        """
        Retrieves the historical market value of each holding.

        Returns:
            history (DataFrame): A pandas DataFrame with a (Date, Symbol) MultiIndex
            that tracks the value of each holding over time.
        """
        return self._history
    
    def getCashHistory(self) -> DataFrame:
        """
        Retrieves the historical value of the portfolio's cash balance.

        Returns:
            cashHistory (DataFrame): A pandas DataFrame indexed by Date that tracks
            the cash value over time.
        """
        return self._cashHistory

    def _updateValue(self, marketData: DataFrame):
        """
        Updates and records the current value of all holdings and cash based on the market data.

        Parameters:
            marketData (DataFrame): A DataFrame containing market prices for the
            current date, indexed by (Date, Symbol).
        """
        date = marketData.index.get_level_values("Date")[-1]
        self._cashHistory.loc[date, "Value"] = self._cash
        # Increment through each holding and update by current market price
        for symbol, shares in self._holdings.items():
            self._history.loc[(date, symbol), "Value"] = shares * marketData.loc[(date, symbol), "Close"]

            

    def _executeTrades(self, marketData: DataFrame, tradeReqeusts: List[TradeRequest]):
        """
        Executes a list of trade requests based on current market data. It validates 
        trades against available shares or cash and updates the portfolio's state accordingly.

        Parameters:
            marketData (DataFrame): A DataFrame with current market prices, used to 
            determine the execution price of trades.
            tradeRequests (List[TradeRequest]): A list of buy or sell requests to be 
            executed.
        """
        date = marketData.index.get_level_values("Date")[-1]
        buyRequests = []
        for request in tradeReqeusts:
            if request.side == "BUY": # Execute SELL orders first to free up cash
                buyRequests.append(request)
                continue
            symbol = request.symbol
            sharePrice = marketData.loc[(date, symbol), "Close"]
            # Can only sell symbols that are being hold
            if symbol not in self._holdings:
                continue
            # Can't sell if requested shares is greater than shares held
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
            # Can't buy if request value is greater than current cash
            if value > self._cash:
                continue
            # Buy
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
        """
        Sells all current holdings in the portfolio.

        Parameters:
            marketData (DataFrame): A DataFrame with current market prices,
            used to determine the sale price.
        """
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

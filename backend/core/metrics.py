from pandas import DataFrame
import pandas as pd

from core.portfolio import Portfolio


class Metrics:
    def __init__(self, marketData: DataFrame, portfolio: Portfolio):
        """
        Initializes the metrics calculation object.

        Parameters:
            marketData (DataFrame): The complete market data used in the backtest.
            portfolio (Portfolio): The portfolio object after the backtest is complete.
        """
        self.marketData = marketData
        self.portfolio = portfolio

    def getProfitLoss(self):
        """
        Calculates the total profit or loss for the entire backtest period.

        Returns:
            pnl (float): The total profit or loss in currency units.
        """
        return self.portfolio.getCash() - self.portfolio.getInitialCash()

    def getAnnualizedReturn(self):
        """
        Calculates the annualized rate of return for the entire backtest period.

        Returns:
            annualizedReturn (float): The annualized return as a decimal.
        """
        if self.marketData.empty:
            return 0.0
        duration = self.marketData.index.get_level_values("Date")[-1] - self.marketData.index.get_level_values("Date")[0]
        cumulativeReturn = self.getProfitLoss() / self.portfolio._initialCash
        durationYears = duration.days / 365.25
        annualizedReturn = pow((1 + cumulativeReturn), (1 / durationYears)) - 1
        return annualizedReturn

    def getMaxDrawdown(self):
        """
        Calculates the maximum drawdown of the portfolio's value.

        Returns:
            mdd (float): The maximum drawdown as a positive decimal.
        """
        accountValue = self.portfolio.getHistory().groupby(level="Date").sum()["Value"]
        accountValue += self.portfolio.getCashHistory()["Value"]
        rollingPeak = accountValue.cummax()
        drawdown = (rollingPeak - accountValue) / rollingPeak.replace(0, None)
        mdd = drawdown.max()
        if not pd.notna(mdd):
            mdd = 0
        return mdd


    def getWinProbability(self):
        """
        Calculates the probability of a closing trade being profitable.

        Returns:
            winRate (float): The win probability as a decimal (e.g., 0.60 for 60%).
        """
        closed = 0
        wins = 0
        positions = pd.DataFrame(columns=["Shares", "Avg Price"])
        for trade in self.portfolio.getTrades():
            symbol = trade.symbol
            if trade.side == "BUY":
                if symbol not in positions.index:
                    positions.loc[symbol] = [trade.shares, trade.sharePrice]
                    continue
                # Calculate average buy price
                shares = positions.loc[symbol, "Shares"]
                avgPrice = positions.loc[symbol, "Avg Price"]
                positionValue = shares * avgPrice
                tradeValue = trade.shares * trade.sharePrice
                
                totalShares = shares + trade.shares
                avgPrice = (positionValue + tradeValue) / (shares + totalShares)
                positions.loc[symbol] = [totalShares, avgPrice]

            elif trade.side == "SELL":
                if symbol not in positions.index:
                    continue # Shouldn't happen, but just in case
                buyPrice = positions.loc[symbol, "Avg Price"]
                positions.loc[symbol, "Shares"] -= trade.shares
                # If positive trade, win
                if trade.sharePrice > buyPrice:
                    wins += 1
                closed += 1
        if closed == 0:
            return 0
        return wins / closed

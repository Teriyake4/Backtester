from pandas import DataFrame
import pandas as pd

from core.portfolio import Portfolio


class Metrics:
    def __init__(self, marketData: DataFrame, portfolio: Portfolio):
        self.marketData = marketData
        self.portfolio = portfolio

    def getProfitLoss(self):
        return self.portfolio.getCash() - self.portfolio.getInitialCash()

    def getAnnualizedReturn(self):
        if self.marketData.empty:
            return 0.0
        duration = self.marketData.index.get_level_values("Date")[-1] - self.marketData.index.get_level_values("Date")[0]
        cumulativeReturn = self.getProfitLoss() / self.portfolio._initialCash
        durationYears = duration.days / 365.25
        annualizedReturn = pow((1 + cumulativeReturn), (1 / durationYears)) - 1
        return annualizedReturn

    def getMaxDrawdown(self):
        accountValue = self.portfolio.getHistory().groupby(level="Date").sum()["Value"]
        accountValue += self.portfolio.getCashHistory()["Value"]
        rollingPeak = accountValue.cummax()
        drawdown = (rollingPeak - accountValue) / rollingPeak.replace(0, None)
        mdd = drawdown.max()
        if not pd.notna(mdd):
            mdd = 0
        return mdd


    def getWinProbability(self):
        closed = 0
        wins = 0
        positions = pd.DataFrame(columns=["Shares", "Avg Price"])
        for trade in self.portfolio.getTrades():
            symbol = trade.symbol
            if trade.side == "BUY":
                if symbol not in positions.index:
                    positions.loc[symbol] = [trade.shares, trade.sharePrice]
                    continue
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
                if trade.sharePrice > buyPrice:
                    wins += 1
                closed += 1
        if closed == 0:
            return 0
        return wins / closed

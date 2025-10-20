from pandas import DataFrame

from backend.core.portfolio import Portfolio


class Metrics:
    def __init__(self, marketData: DataFrame, portfolio: Portfolio):
        self.marketData = marketData
        self.portfolio = portfolio

    def getProfitLoss(self):
        return self.portfolio.getInitialCash - self.portfolio.cash

    def getAnnualizedReturn(self):
        duration = self.marketData.index[-1][0] - self.marketData.index[0][0]
        cumulativeReturn = self.getProfitLoss() / self.portfolio.initialCash
        durationYears = duration.days / 365.25
        annualizedReturn = pow((1 + cumulativeReturn), (1 / durationYears)) - 1
        return annualizedReturn

    def getMaxDrawdown(self):
        pass

    def getWinProbability(self):
        pass
from backend.core.engine import Engine
from backend.interface.backtestRequest import BacktestRequest


class Interface:
    def __init__(self):
        pass

    def backtest(request: BacktestRequest):
        
        Engine.runBacktest(request)

    # backtest([symbols], startDate, endDate, strategy, strategyParams) -> result


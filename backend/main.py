from datetime import datetime
from typing import Any, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.tradeRequest import Side
from core.engine import Engine
from core.strategies.constantPriceThreshold import ConstantPriceThresholdStrategy

class BacktestRequest(BaseModel):
    symbols: List[str]
    startDate: datetime
    endDate: datetime
    startingCash: float
    strategy: str
    strategyParams: Dict[str, Any]

class TradeInfo(BaseModel):
    side: Side
    symbol: str
    shares: int
    price: float
    time: datetime

class BacktestResponse(BaseModel):
    profitLoss: float
    annualizedReturn: float
    maxDrawdown: float
    winProbability: float
    trades: List[TradeInfo]

strategies = {
    "ConstantPriceThresholdStrategy": ConstantPriceThresholdStrategy
}

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Backend running"}

@app.post("/api/backtest", response_model=BacktestResponse)
async def backtest(params: BacktestRequest):
    """
    Post endpoint to run backtest with specified parameters.

    Parameters:
        param (BacktestRequest): Parameters for backtest.
    """
    # Run backtest with parameters
    backtestResults = Engine.runBacktest(
        symbols=params.symbols,
        startDate=params.startDate,
        endDate=params.endDate,
        startingCash=params.startingCash,
        strategyClass=strategies[params.strategy],
        strategyParams=params.strategyParams,
    )
    metrics = [
        "profitLoss",
        "annualizedReturn",
        "maxDrawdown",
        "winProbability"
    ]
    # Assign metrics to ouput
    output = {
        metrics[0]: backtestResults[metrics[0]],
        metrics[1]: backtestResults[metrics[1]],
        metrics[2]: backtestResults[metrics[2]],
        metrics[3]: backtestResults[metrics[3]],
        "trades": []
    }
    # Add trades made during backtest ot ouput
    for trade in backtestResults["portfolio"].getTrades():
        tradeInfo = {
            "side": trade.side,
            "symbol": trade.symbol,
            "shares": trade.shares,
            "price": trade.sharePrice,
            "time": trade.timestamp
        }
        output["trades"].append(tradeInfo)

    return output

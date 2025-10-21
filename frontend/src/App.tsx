import React, { useState } from 'react';
import './App.css';

type ConstantPriceThresholdParams = {
  threshold: number
  daysToClose: number
  quantity: number
}

type BacktestRequest = {
  symbols: string[]
  startDate: Date
  endDate: Date
  startingCash: number
  strategy: string
  strategyParams: ConstantPriceThresholdParams
}

type TradeInfo = {
  side: string
  symbol: string
  shares: number
  price: number
  time: string
}

type BacktestResponse = {
  profitLoss: number
  annualizedReturn: number
  maxDrawdown: number
  winProbability: number
  trades: TradeInfo[]
}

function App() {
  const [response, setResponse] = useState<BacktestResponse | null>(null)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const form = new FormData(event.currentTarget)
    const symbolString = form.get("symbols") as string
    const stratParams: ConstantPriceThresholdParams = {
      threshold: Number(form.get("threshold") as string),
      daysToClose: Number(form.get("daysToClose") as string),
      quantity: Number(form.get("quantity") as string)
    }
    const request: BacktestRequest = {
      symbols: symbolString.split(",").map(s => s.trim()),
      startDate: new Date(form.get("startDate") as string),
      endDate: new Date(form.get("endDate") as string),
      startingCash: Number(form.get("startingCash") as string),
      strategy: "ConstantPriceThresholdStrategy",
      strategyParams: stratParams
    }

    const response = await fetch("http://127.0.0.1:8000/api/backtest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request)
    })

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const result: BacktestResponse = await response.json()
    setResponse(result)
  }

  return (
    <div className="App">
      <div className="App-style">
        <h1>
          Backtester
        </h1>

        <form method="post" onSubmit={handleSubmit}>
        <p>
          <label>
            Symbols: <input name="symbols" defaultValue={"NVDA,GOOGL"} required/>
          </label>
          <div>
            Symbols to backtest on, seperated by commas.
          </div>
        </p>

        <p>
          <label>
            Start Date: <input name="startDate" defaultValue={"2024-1-1"} required/>
          </label>
          <div>
            Start date to start backtest on, inclusive. Year-month-day.
          </div>
        </p>

        <p>
          <label>
            End Date: <input name="endDate" defaultValue={"2025-1-1"} required/>
          </label>
          <div>
            End date to end backtest on, inclusive. Year-month-day.
          </div>
        </p>

        <p>
          <label>
            Starting Cash: <input name="startingCash" defaultValue={1000} required/>
          </label>
          <div>
            Initial cash to start backtest with.
          </div>
        </p>

          <hr/>
          <h3>
            Strategy Parameters:
          </h3>
          <div>
            Parameters for constant price threshold strategy.
          </div>

        <p>
          <label>
            Threshold: <input name="threshold" defaultValue={140} required/>
          </label>
          <div>
            Threshold of symbol price to trigger buy order.
          </div>
        </p>

        <p>
          <label>
            Duration: <input name="daysToClose" defaultValue={10} required/>
          </label>
          <div>
            Duration to hold and then sell symbol.
          </div>
        </p>

          <p>
            <label>
              Quantity: <input name="quantity" defaultValue={5} required/>
            </label>
            <div>
              Number of shares to buy and sell at a time.
            </div>
          </p>
          
          <hr/>

          <button type="submit" className="submit-button">
            Run backtest
          </button>
        </form>

        {response && (
          <div>
            <h2>Backtest Results</h2>
            <p><strong>Profit/Loss: </strong> ${response.profitLoss.toFixed(2)}</p>
            <p><strong>Annualized Return: </strong> {(response.annualizedReturn * 100).toFixed(4)}%</p>
            <p><strong>Max Drawdown: </strong> {(response.maxDrawdown * 100).toFixed(4)}%</p>
            <p><strong>Win Probability: </strong> {(response.winProbability * 100).toFixed(4)}%</p>
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Symbol</th>
                  <th>Side</th>
                  <th>Shares</th>
                  <th>Price</th>
                  <th>Total Value</th>
                </tr>
              </thead>
              <tbody>
                {/* 4. Map over the trades array to create a table row for each trade */}
                {response.trades.map((trade, index) => (
                  <tr key={index} className={trade.side}>
                    <td>{new Date(trade.time).toDateString()}</td>
                    <td>{trade.symbol}</td>
                    <td>{trade.side}</td>
                    <td>{trade.shares}</td>
                    <td>${trade.price.toFixed(2)}</td>
                    <td>${(trade.shares * trade.price).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>
      <footer className="App-footer"/>
    </div>
  );
}

export default App;

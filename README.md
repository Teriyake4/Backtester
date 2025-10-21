# Backtester
A full-stack web application designed to backtest and visualize the performance of trading algorithms. 
Stock symbols, date range, and strategy-specific parameters can be selected to see how a trading strategy would have performed.

The backend uses Python and FastAPI which handles data ingestion and querying from the ingestion script or the database respectively, 
backtesting logic, and performance calculations. Data is stored locally on the SQLite database.
The frontend uses React and TypeScript for user interaction and displaying metrics.

# Setup
Run The following commands to setup the backend environment.
```
cd backend
conda env create -f environment.yml
conda activate backtester
```
To run the backend.
```
fastapi dev main.py
```

Run The following commands to setup the frontend environment.
```
cd frontend
npm install
```
To run the frontend.
```
npm start
```

# Ingester Script
To run the ingester script.
```
cd backend
python /processing/ingester.py --symbol [symbol] --start [YYYY-mm-dd] --end [YYYY-mm-dd]
```

# Strategies
All strategies implement the base Strategy class. The next function will process the strategy for each increment in data. The data availible to
the strategy is the simulated market data up to the point in time it's being called and the current portolio. The market data is a multi-index 
Pandas Dataframe set as (Date, Symbol) in ascending order (lowest index: past, highest index: present) and contains the following columns: 
Open, High, Low, Close, Adj Close, and Volume. The portolio is delivered as an object with getter methods to access, the following data: 
inital cash, current cash, holdings, trade history, portoflio value history by symbol, cash history. To look at an example strategy, see 
ConstantPriceThresholdStrategy class which buys a specified quantity when a symbol strikes a predetermined threshold from below and holds for a 
specified amount of time.

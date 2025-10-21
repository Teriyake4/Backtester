# Backtester
A full-stack web application designed to backtest and visualize the performance of trading algorithms. 
Stock symbols, date range, and strategy-specific parameters can be selected to see how a trading strategy would have performed.

The backend uses Python and FastAPI which handles data ingestion and querying from the ingestion script or the database respectively, 
backtesting logic, and performance calculations. The database used is SQLite.
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


Run The following commands to setup the fronend environment.
```
cd frontend
npm install
```
To run the frontend.
```
npm start
```

# Ingester Script
To run the ingester script
```
cd backend
python /processing/ingester.py --symbol [symbol] --start [YYYY-mm-dd] --end [YYYY-mm-dd]
```

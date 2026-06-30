# Alpaca Algorithmic Trading Backtesting Platform

A complete, modular algorithmic trading backtesting platform using Python and the Alpaca Historical Market Data API.

## Features
- **Data Acquisition:** Downloads 5 years of daily OHLCV data using `alpaca-py` (with a seamless fallback to `yfinance`).
- **Technical Indicators:** Calculates SMA, EMA, MACD, RSI, Bollinger Bands, and OBV using `pandas-ta`.
- **Strategies:** Implements Trend Following, Mean Reversion, and a Custom hybrid strategy.
- **Backtesting Engine:** Vectorized backtesting evaluating Total Return, CAGR, Volatility, Sharpe, Sortino, Max Drawdown, and Win Rate.
- **Visualizations:** Generates Price Charts (with buy/sell signals), Equity Curves, and Drawdown comparisons using `matplotlib`.

## Setup Instructions

1. **Ensure all files are in the same directory.**

2. **Install Dependencies:**
   Run the following command to install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys (Optional but Recommended):**
   Set your Alpaca API keys as environment variables. If not set, the platform will automatically fall back to using `yfinance`.
   
   **Mac/Linux:**
   ```bash
   export ALPACA_API_KEY='your_api_key'
   export ALPACA_SECRET_KEY='your_secret_key'
   ```
   **Windows (Command Prompt):**
   ```cmd
   set ALPACA_API_KEY=your_api_key
   set ALPACA_SECRET_KEY=your_secret_key
   ```

4. **Run the Backtester:**
   ```bash
   python main.py
   ```

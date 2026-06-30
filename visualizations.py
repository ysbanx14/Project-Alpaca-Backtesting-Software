import matplotlib.pyplot as plt

def plot_price_chart(df, signals_df, strategy_name="Strategy"):
    """
    Plots the asset price, Bollinger Bands, 50-day SMA, and overlays Buy/Sell markers.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['close'], label='Close Price', alpha=0.5)
    if 'SMA_50' in df.columns:
        plt.plot(df.index, df['SMA_50'], label='50-day SMA', alpha=0.7)
    
    if 'BB_Upper' in df.columns and 'BB_Lower' in df.columns:
        plt.plot(df.index, df['BB_Upper'], label='Upper BB', color='gray', alpha=0.3, linestyle='--')
        plt.plot(df.index, df['BB_Lower'], label='Lower BB', color='gray', alpha=0.3, linestyle='--')
        plt.fill_between(df.index, df['BB_Lower'], df['BB_Upper'], color='gray', alpha=0.1)

    # Trades: 1 is Buy, -1 is Sell
    buys = signals_df[signals_df['trades'] == 1.0]
    sells = signals_df[signals_df['trades'] == -1.0]
    
    plt.scatter(buys.index, df.loc[buys.index, 'close'], marker='^', color='green', s=100, label='Buy Signal')
    plt.scatter(sells.index, df.loc[sells.index, 'close'], marker='v', color='red', s=100, label='Sell Signal')
    
    plt.title(f"{strategy_name} - Price Chart & Signals")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_equity_curves(results_dict, initial_capital=100000.0):
    """
    Plots and compares the portfolio value over time for all strategies.
    results_dict: {'Strategy Name': result_df}
    """
    plt.figure(figsize=(14, 7))
    for name, res_df in results_dict.items():
        plt.plot(res_df.index, res_df['equity'], label=name)
        
    plt.axhline(y=initial_capital, color='r', linestyle='--', alpha=0.5)
    plt.title("Equity Curve Comparison")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_drawdowns(results_dict):
    """
    Plots and compares the underwater/drawdown curves for all strategies.
    """
    plt.figure(figsize=(14, 7))
    for name, res_df in results_dict.items():
        running_max = res_df['equity'].cummax()
        drawdown = (res_df['equity'] - running_max) / running_max
        plt.plot(res_df.index, drawdown * 100, label=name)
        plt.fill_between(res_df.index, drawdown * 100, 0, alpha=0.1)
        
    plt.title("Drawdown Comparison (%)")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_individual_trade(df, trade_info, buffer_days=5):
    """
    Plots a zoomed-in view of a single trade.
    trade_info: A dictionary containing {'entry_date': ..., 'exit_date': ..., 'strategy': ...}
    buffer_days: Number of days to show before entry and after exit for visual context.
    """
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # 1. Parse the target dates
    target_entry = pd.to_datetime(trade_info['entry_date'])
    target_exit = pd.to_datetime(trade_info['exit_date'])
    
    # 2. Find the exact timestamps in the DataFrame nearest to our targets
    # This bypasses the KeyError caused by hour/minute mismatches
    actual_entry_dt = df.index[df.index.get_indexer([target_entry], method='nearest')[0]]
    actual_exit_dt = df.index[df.index.get_indexer([target_exit], method='nearest')[0]]
    
    # 3. Calculate integer bounds for the zoom window
    entry_idx = df.index.get_loc(actual_entry_dt)
    exit_idx = df.index.get_loc(actual_exit_dt)
    
    plot_start = df.index[max(0, entry_idx - buffer_days)]
    plot_end = df.index[min(len(df) - 1, exit_idx + buffer_days)]
    
    trade_df = df.loc[plot_start:plot_end]
    
    plt.figure(figsize=(12, 6))
    plt.plot(trade_df.index, trade_df['close'], label='Close Price', color='blue', alpha=0.6)
    
    # Plot technical lines if they exist in the dataframe
    if 'SMA_50' in trade_df.columns:
        plt.plot(trade_df.index, trade_df['SMA_50'], label='50-day SMA', linestyle='--', alpha=0.5)
    if 'BB_Upper' in trade_df.columns and 'BB_Lower' in trade_df.columns:
        plt.plot(trade_df.index, trade_df['BB_Upper'], color='gray', linestyle=':', alpha=0.4)
        plt.plot(trade_df.index, trade_df['BB_Lower'], color='gray', linestyle=':', alpha=0.4)
    
    # 4. Highlight entry and exit points using the actual index datetimes
    plt.scatter(actual_entry_dt, df.loc[actual_entry_dt, 'close'], color='green', marker='^', s=150, label=f"Entry: {actual_entry_dt.date()}")
    plt.scatter(actual_exit_dt, df.loc[actual_exit_dt, 'close'], color='red', marker='v', s=150, label=f"Exit: {actual_exit_dt.date()}")
    
    # Highlight the duration of the trade
    plt.axvspan(actual_entry_dt, actual_exit_dt, color='green', alpha=0.1, label='Trade Duration')
    
    plt.title(f"{trade_info.get('strategy', 'Strategy')} - Trade Zoom-In")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

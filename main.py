import pandas as pd
from tabulate import tabulate

from data_loader import fetch_data
from indicators import calculate_indicators
from strategies import strategy_1_trend_following, strategy_2_mean_reversion, strategy_3_custom, strategy_4_ascending_triangle
from backtester import Backtester
from visualizations import plot_price_chart, plot_equity_curves, plot_drawdowns, plot_individual_trade

def main():
    ticker = "SPY"
    print(f"--- Starting Backtest for {ticker} ---")
    
    # 1. Fetch Data
    df = fetch_data(ticker=ticker, years=5)
    if df.empty:
        print("Failed to fetch data. Exiting.")
        return
    print(f"Fetched {len(df)} days of data.")
    
    # 2. Calculate Indicators
    df = calculate_indicators(df)
    # Drop NaNs that are created by indicator lookbacks
    df = df.dropna()
    print("Calculated technical indicators.")
    
    # 3. Generate Signals for Strategies
    s1_signals = strategy_1_trend_following(df)
    s2_signals = strategy_2_mean_reversion(df)
    s3_signals = strategy_3_custom(df)
    s4_signals = strategy_4_ascending_triangle(df)
    buy_hold_signals = pd.Series(1, index=df.index) # Always invested
    
    # 4. Run Backtester
    backtester = Backtester(initial_capital=100000.0)
    
    results = {}
    metrics_list = []
    
    strategies = {
        'Buy & Hold': buy_hold_signals,
        'Trend Following': s1_signals,
        'Mean Reversion': s2_signals,
        'Custom Strategy': s3_signals,
        'Ascending Triangle': s4_signals
    }
    
    print("Running simulations...")
    for name, signals in strategies.items():
        metrics, res_df = backtester.run(df, signals)
        results[name] = res_df
        metrics['Strategy'] = name
        metrics_list.append(metrics)
        
    # 5. Print Metrics Table
    # Reorder columns to put 'Strategy' first
    cols = ['Strategy', 'Total Return', 'CAGR', 'Annualized Volatility', 'Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown', 'Win Rate']
    metrics_df = pd.DataFrame(metrics_list)[cols]
    
    print("\n=== Strategy Performance Summary ===")
    print(tabulate(metrics_df, headers='keys', tablefmt='psql', showindex=False))
    
    # 6. Generate Charts
    print("\nGenerating charts (close each window to proceed to the next chart)...")
    
    # Let's plot Price Chart for Strategy 3 as an example
    plot_price_chart(df, results['Custom Strategy'], strategy_name="Custom Strategy")
    
    # Plot Equity Curves
    plot_equity_curves(results)
    
    # Plot Drawdowns
    plot_drawdowns(results)
    
    print("--- Backtest Complete ---")

    # Interactive Trade Inspection Loop
    while True:
        print("\n--- Interactive Trade Inspector ---")
        strategy_names = list(results.keys())
        for i, s_name in enumerate(strategy_names):
            print(f"{i+1}. {s_name}")
        print("q. Quit")
        
        choice = input("Select a strategy to inspect trades (enter number or 'q'): ").strip()
        if choice.lower() == 'q':
            break
            
        try:
            strat_idx = int(choice) - 1
            if strat_idx < 0 or strat_idx >= len(strategy_names):
                print("Invalid selection. Try again.")
                continue
            
            selected_strat = strategy_names[strat_idx]
            trades_log = results[selected_strat].attrs.get('trades_log', [])
            
            if not trades_log:
                print(f"No completed trades logged for {selected_strat}.")
                continue
                
            print(f"\n--- First 10 Trades for {selected_strat} ---")
            for i, trade in enumerate(trades_log[:10]):
                print(f"{i+1}. Entry: {trade['entry_date']} | Exit: {trade['exit_date']} | Return: {trade['return']*100:.2f}%")
                
            trade_choice = input(f"Select a trade to view (1-{min(10, len(trades_log))}) or 'b' to go back: ").strip()
            if trade_choice.lower() == 'b':
                continue
                
            trade_idx = int(trade_choice) - 1
            if trade_idx < 0 or trade_idx >= min(10, len(trades_log)):
                print("Invalid trade selection.")
                continue
                
            trade_info = trades_log[trade_idx].copy()
            trade_info['strategy'] = selected_strat
            
            print(f"Plotting trade {trade_choice}...")
            plot_individual_trade(df, trade_info, buffer_days=5)
            
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()

import pandas as pd

def strategy_1_trend_following(df):
    """
    Strategy 1 (Trend Following):
    Buy when MACD > MACD Signal AND close price > 50-day SMA.
    Sell when MACD < MACD Signal.
    """
    signals = pd.Series(0, index=df.index)
    in_position = False
    
    for i in range(1, len(df)):
        # Buy Condition
        if (df['MACD'].iloc[i] > df['MACD_Signal'].iloc[i] and 
            df['close'].iloc[i] > df['SMA_50'].iloc[i] and 
            not in_position):
            signals.iloc[i] = 1
            in_position = True
        # Sell Condition
        elif df['MACD'].iloc[i] < df['MACD_Signal'].iloc[i] and in_position:
            signals.iloc[i] = 0
            in_position = False
        else:
            signals.iloc[i] = 1 if in_position else 0
            
    return signals

def strategy_2_mean_reversion(df):
    """
    Strategy 2 (Mean Reversion):
    Buy when RSI < 30 AND price is below the Lower Bollinger Band.
    Sell when RSI > 70 AND price is above the Upper Bollinger Band.
    """
    signals = pd.Series(0, index=df.index)
    in_position = False
    
    for i in range(1, len(df)):
        if (df['RSI_14'].iloc[i] < 30 and 
            df['close'].iloc[i] < df['BB_Lower'].iloc[i] and 
            not in_position):
            signals.iloc[i] = 1
            in_position = True
        elif (df['RSI_14'].iloc[i] > 70 and 
              df['close'].iloc[i] > df['BB_Upper'].iloc[i] and 
              in_position):
            signals.iloc[i] = 0
            in_position = False
        else:
            signals.iloc[i] = 1 if in_position else 0
            
    return signals

def strategy_3_custom(df):
    """
    Strategy 3 (Custom Strategy):
    Combines Trend (200 SMA), Momentum (14 RSI), and Volume (OBV).
    Buy when: Close > 200 SMA AND RSI < 55 AND OBV > 50-day OBV SMA.
    Sell when: RSI > 70 OR Close < 200 SMA.
    """
    import pandas as pd
    
    signals = pd.Series(0, index=df.index)
    in_position = False
    
    # Lengthen the OBV SMA to 50 days so short pullbacks don't break the volume trend
    obv_sma = df['OBV'].rolling(window=50).mean()
    
    for i in range(1, len(df)):
        # Buy Condition
        if (df['close'].iloc[i] > df['SMA_200'].iloc[i] and 
            df['RSI_14'].iloc[i] < 55 and 
            df['OBV'].iloc[i] > obv_sma.iloc[i] and 
            not in_position):
            signals.iloc[i] = 1
            in_position = True
            
        # Sell Condition
        elif (df['RSI_14'].iloc[i] > 70 or df['close'].iloc[i] < df['SMA_200'].iloc[i]) and in_position:
            signals.iloc[i] = 0
            in_position = False
            
        # Hold Condition
        else:
            signals.iloc[i] = 1 if in_position else 0
            
    return signals

def strategy_4_ascending_triangle(df, window=20):
    """
    Strategy 4 (Ascending Triangle Breakout):
    Identifies a horizontal resistance line and a rising support line.
    Buys when the close price breaks above the resistance.
    Sells when the close price drops below the recent support.
    """
    import pandas as pd
    
    signals = pd.Series(0, index=df.index)
    in_position = False
    
    # 1. Define Resistance: The highest high over the last 'window' days.
    resistance = df['high'].rolling(window=window).max().shift(1)
    
    # 2. Define Rising Support: Compare the lowest low of the most recent 10 days
    # against the lowest low of the 10 days before that.
    half_window = window // 2
    recent_support = df['low'].rolling(window=half_window).min().shift(1)
    prior_support = df['low'].rolling(window=half_window).min().shift(half_window + 1)
    
    start_index = window + 2 
    
    for i in range(start_index, len(df)):
        is_support_rising = recent_support.iloc[i] > prior_support.iloc[i]
        is_breakout = df['close'].iloc[i] > resistance.iloc[i]
        
        if not in_position and is_support_rising and is_breakout:
            signals.iloc[i] = 1
            in_position = True
        elif in_position and df['close'].iloc[i] < recent_support.iloc[i]:
            signals.iloc[i] = 0
            in_position = False
        else:
            signals.iloc[i] = 1 if in_position else 0
            
    return signals

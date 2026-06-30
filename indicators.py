import pandas as pd
import pandas_ta as ta

def calculate_indicators(df):
    """
    Calculates technical indicators on the given OHLCV DataFrame.
    Calculates: SMA (50), EMA (20), EMA (50), MACD, RSI (14), Bollinger Bands (20, 2), OBV.
    """
    # Ensure columns exist
    required = ['open', 'high', 'low', 'close', 'volume']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # 1. SMA (Trend) - 50 period
    df['SMA_50'] = ta.sma(df['close'], length=50)

    # 2. EMA (Trend) - 20 period and 50 period for custom strategy
    df['EMA_20'] = ta.ema(df['close'], length=20)
    df['EMA_50'] = ta.ema(df['close'], length=50)

    # 3. MACD (Trend)
    macd = ta.macd(df['close'])
    if macd is not None and not macd.empty:
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_Signal'] = macd['MACDs_12_26_9']
        df['MACD_Hist'] = macd['MACDh_12_26_9']

    # 4. RSI (Momentum) - 14 period
    df['RSI_14'] = ta.rsi(df['close'], length=14)

    # 5. Bollinger Bands (Volatility) - 20 period, 2 std
    bbands = ta.bbands(df['close'], length=20, std=2)
    if bbands is not None and not bbands.empty:
        df['BB_Lower'] = bbands['BBL_20_2.0_2.0']
        df['BB_Middle'] = bbands['BBM_20_2.0_2.0']
        df['BB_Upper'] = bbands['BBU_20_2.0_2.0']

    # 6. OBV (On-Balance Volume)
    df['OBV'] = ta.obv(df['close'], df['volume'])

    return df

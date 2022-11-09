import yfinance as yf
from datetime import datetime
from data.schemas.df_schema import GraphSchema

# GET FX RATES FROM YAHOO
def fx_rate(ticker_list, start_date, end_date):
    tickers_yf = [yf.Ticker(ticker) for ticker in ticker_list]
    fx_data = [ticker_yf.history(start=start_date, end=end_date, interval="1d") for ticker_yf in tickers_yf]
    [df.drop(columns=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], inplace=True) for df in fx_data]
    [df.reset_index(inplace=True) for df in fx_data]
    [df.rename(columns={'Close': f'{GraphSchema.FX_RATE}'}, inplace=True) for df in fx_data]

    for df in fx_data:
        df[GraphSchema.DATE] = df[GraphSchema.DATE].dt.strftime("%Y-%m-%d")

        for row in range(0, len(df)):
            df.loc[row, GraphSchema.DATE] = datetime.strptime(df.loc[row, GraphSchema.DATE], "%Y-%m-%d").date()

    return fx_data

# GET FX NOTATIONS FROM TICKERS
def fx_list(ticker_list):
    tickers_yf = [yf.Ticker(ticker) for ticker in ticker_list]
    list_fx = [ticker_yf.info['currency'] for ticker_yf in tickers_yf]

    return list_fx

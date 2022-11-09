import yfinance as yf
import pandas as pd
import datetime
import plotly.express as px

# GET DATA FROM YAHOO
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
last_month = yesterday.replace(day=1) - datetime.timedelta(days=1)

geo_tickers = ['^GSPC', '^STOXX', '^FTSE', 'EEM', 'ACWI']
geo_areas = ['US', 'Europe', 'UK', 'Emerging Markets', 'World']

def data(ticker_list):
    tickers_yf = [yf.Ticker(ticker) for ticker in ticker_list]

    data_mtd = [ticker_yf.history(start=last_month, end=today, interval="1d") for ticker_yf in tickers_yf]
    data_mtd = [df.drop(columns=['High', 'Low', 'Volume', 'Dividends', 'Stock Splits']) for df in data_mtd]

    data_ytd = [ticker_yf.history(start="2021-12-31", end="2022-10-26", interval="1d") for ticker_yf in tickers_yf]
    data_ytd = [df.drop(columns=['High', 'Low', 'Volume', 'Dividends', 'Stock Splits']) for df in data_ytd]

    return data_mtd, data_ytd

geo_data_mtd, geo_data_ytd = data(geo_tickers)

# CREATE COMPLETE YTD DATAFRAME (incl returns)
for count, df in enumerate(geo_data_ytd):
    df.reset_index(inplace=True)
    df['Area'] = geo_areas[count]
    df['Return%'] = df['Close']/df['Open'] - 1
    df['Return%'] = df['Return%'].fillna(0)
    df['Return'] = 1
    for row in range(1, len(df)):
        df.loc[row, 'Return'] = df.loc[row-1, 'Return'] * (1 + df.loc[row, 'Return%'])

geo_data_ytd = pd.concat(geo_data_ytd)

# PLOT YTD GRAPH
ytd_graph = px.line(
            geo_data_ytd,
            x="Date",
            y="Return",
            color='Area',
            log_y=True
)

ytd_graph.show()


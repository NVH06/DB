import yfinance as yf
import pandas as pd
from datetime import datetime
from data.fx_data import fx_rate, fx_list
from data.schemas.df_schema import GraphSchema
from data.schemas.data_id_schema import TickerSchema, CategorySchema
from data.schemas.input_schema import DateSchema, FXInputSchema


# GET FX DATA
fx_rates = fx_rate(TickerSchema.FX, DateSchema.START_DATE_SEL, DateSchema.END_DATE_SEL)
geo_data_fx_list = fx_list(TickerSchema.GEO)

# GET RAW DATA FROM YAHOO
def data_graph_raw(ticker_list, start_date, end_date):
    tickers_yf = [yf.Ticker(ticker) for ticker in ticker_list]

    graph_data_raw = [ticker_yf.history(start=start_date, end=end_date, interval="1d") for ticker_yf in tickers_yf]
    [df.drop(columns=['High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], inplace=True) for df in graph_data_raw]
    [df.reset_index(inplace=True) for df in graph_data_raw]

    for df in graph_data_raw:
        df[GraphSchema.DATE] = df[GraphSchema.DATE].dt.strftime("%Y-%m-%d")

        for row in range(0, len(df)):
            df.loc[row, GraphSchema.DATE] = datetime.strptime(df.loc[row, GraphSchema.DATE], "%Y-%m-%d").date()

    return graph_data_raw

geo_data_graph_raw = data_graph_raw(TickerSchema.GEO, DateSchema.START_DATE_SEL, DateSchema.END_DATE_SEL)    # make start/end date dynamic

# CREATE COMPLETE DATA
def data_graph(cat_schema, raw_df, fx_input, fx_list_df, fx_rates_df):
    data_df = []
    for count, df in enumerate(raw_df):
        df[GraphSchema.CATEGORY] = cat_schema[count]
        df[GraphSchema.FX] = fx_list_df[count]

        if fx_input == fx_list_df[count]:
            df[GraphSchema.FX_RATE] = 1
        if fx_input != fx_list_df[count] and fx_input == 'EUR':
            if fx_list_df[count] == 'USD':
                df = df.merge(fx_rates_df[0], on=GraphSchema.DATE, how='left')
            if fx_list_df[count] == 'GBP':
                df = df.merge(fx_rates_df[1], on=GraphSchema.DATE, how='left')
        if fx_input != fx_list_df[count] and fx_input == 'USD':
            if fx_list_df[count] == 'EUR':
                df = df.merge(fx_rates_df[0], on=GraphSchema.DATE, how='left')
            if fx_list_df[count] == 'GBP':
                df = df.merge(fx_rates_df[1], on=GraphSchema.DATE, how='left')

        df[GraphSchema.OPEN_FX] = df[GraphSchema.OPEN]/df[GraphSchema.FX_RATE]
        df[GraphSchema.CLOSE_FX] = df[GraphSchema.CLOSE]/df[GraphSchema.FX_RATE]

        df[GraphSchema.RETURNPCT] = df[GraphSchema.CLOSE_FX] / df[GraphSchema.OPEN_FX] - 1
        df[GraphSchema.RETURNPCT] = df[GraphSchema.RETURNPCT].fillna(0)
        df[GraphSchema.RETURN1] = 1
        for row in range(1, len(df)):
            df.loc[row, GraphSchema.RETURN1] = (df.loc[row - 1, GraphSchema.RETURN1] * (1 + df.loc[row, GraphSchema.RETURNPCT]))

        df[GraphSchema.RETURN] = round((df[GraphSchema.RETURN1] - 1) * 100, 2)
        data_df.append(df)

    graph_data = pd.concat(data_df)
    return graph_data

geo_data_graph = data_graph(CategorySchema.GEO, geo_data_graph_raw, FXInputSchema.FX, geo_data_fx_list, fx_rates)

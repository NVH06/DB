import yfinance as yf
import pandas as pd
import datetime
from data.fx_data import fx_rate, fx_list
from data.schemas.df_schema import TableDataSchema, TableSchema
from data.schemas.data_id_schema import TickerSchema, CategorySchema
from data.schemas.input_schema import DateSchema, FXInputSchema

# GET FX DATA
fx_rates = fx_rate(TickerSchema.FX, DateSchema.YEAR_START, DateSchema.END_DATE_SEL)
geo_data_fx_list = fx_list(TickerSchema.GEO)

# GET RAW DATA FROM YAHOO
def data_table_raw(ticker_list, start_date, end_date):
    tickers_yf = [yf.Ticker(ticker) for ticker in ticker_list]

    table_data_raw = [ticker_yf.history(start=start_date, end=end_date, interval="1d") for ticker_yf in tickers_yf]
    [df.drop(columns=['High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], inplace=True) for df in table_data_raw]
    [df.reset_index(inplace=True) for df in table_data_raw]

    for df in table_data_raw:
        df[TableDataSchema.DATE] = df[TableDataSchema.DATE].dt.strftime("%Y-%m-%d")

        for row in range(0, len(df)):
            df.loc[row, TableDataSchema.DATE] = datetime.datetime.strptime(df.loc[row, TableDataSchema.DATE], "%Y-%m-%d").date()

    return table_data_raw

geo_data_table_raw = data_table_raw(TickerSchema.GEO, DateSchema.YEAR_START, DateSchema.END_DATE_SEL)


# CREATE COMPLETE DATA
def data_table_complete(raw_df, cat_schema, fx_input, fx_list_df, fx_rates_df):
    data_df = []
    for count, df in enumerate(raw_df):
        df[TableDataSchema.CATEGORY] = cat_schema[count]
        df[TableDataSchema.FX] = fx_list_df[count]

        if fx_input == fx_list_df[count]:
            df[TableDataSchema.FX_RATE] = 1
        if fx_input != fx_list_df[count] and fx_input == 'EUR':
            if fx_list_df[count] == 'USD':
                df = df.merge(fx_rates_df[0], on=TableDataSchema.DATE, how='left')
            if fx_list_df[count] == 'GBP':
                df = df.merge(fx_rates_df[1], on=TableDataSchema.DATE, how='left')
        if fx_input != fx_list_df[count] and fx_input == 'USD':
            if fx_list_df[count] == 'EUR':
                df = df.merge(fx_rates_df[0], on=TableDataSchema.DATE, how='left')
            if fx_list_df[count] == 'GBP':
                df = df.merge(fx_rates_df[1], on=TableDataSchema.DATE, how='left')

        df[TableDataSchema.OPEN_FX] = df[TableDataSchema.OPEN] / df[TableDataSchema.FX_RATE]
        df[TableDataSchema.CLOSE_FX] = df[TableDataSchema.CLOSE] / df[TableDataSchema.FX_RATE]

        data_df.append(df)

    graph_data = pd.concat(data_df)
    graph_data.reset_index(inplace=True)

    return graph_data

geo_data_table_complete = data_table_complete(geo_data_table_raw,
                                              CategorySchema.GEO,
                                              FXInputSchema.FX,
                                              geo_data_fx_list,
                                              fx_rates)
# print(geo_data_table_complete[geo_data_table_complete['Category'] == 'Europe'])
# exit()

def table(data_complete, cat_schema, day_date, mtd_date, ytd_date, year_date):
    df = pd.DataFrame(columns=TableSchema.COLUMNS)
    df[TableSchema.CATEGORY] = cat_schema

    yday_col = []
    mtd_col = []
    ytd_col = []
    year_col = []

    for cat in cat_schema:
        df_cat = data_complete[data_complete[TableDataSchema.CATEGORY] == cat]

        day_date_act = df_cat.loc[(df_cat[TableDataSchema.DATE] - day_date).abs().idxmin(), TableDataSchema.DATE]
        mtd_date_act = df_cat.loc[(df_cat[TableDataSchema.DATE] - mtd_date).abs().idxmin(), TableDataSchema.DATE]
        ytd_date_act = df_cat.loc[(df_cat[TableDataSchema.DATE] - ytd_date).abs().idxmin(), TableDataSchema.DATE]
        year_date_act = df_cat.loc[(df_cat[TableDataSchema.DATE] - year_date).abs().idxmin(), TableDataSchema.DATE]

        yday_row = data_complete[(data_complete[TableDataSchema.DATE] == day_date_act) & (data_complete[TableDataSchema.CATEGORY] == cat)].index
        mtd_row = data_complete[(data_complete[TableDataSchema.DATE] == mtd_date_act) & (data_complete[TableDataSchema.CATEGORY] == cat)].index
        ytd_row = data_complete[(data_complete[TableDataSchema.DATE] == ytd_date_act) & (data_complete[TableDataSchema.CATEGORY] == cat)].index
        year_row = data_complete[(data_complete[TableDataSchema.DATE] == year_date_act) & (data_complete[TableDataSchema.CATEGORY] == cat)].index

        yday_return = round(((data_complete.loc[yday_row, TableDataSchema.CLOSE_FX].item() / data_complete.loc[yday_row, TableDataSchema.OPEN_FX].item()) - 1) * 100, 2)
        mtd_return = round(((data_complete.loc[yday_row, TableDataSchema.CLOSE_FX].item() / data_complete.loc[mtd_row, TableDataSchema.CLOSE_FX].item()) - 1) * 100, 2)
        ytd_return = round(((data_complete.loc[yday_row, TableDataSchema.CLOSE_FX].item() / data_complete.loc[ytd_row, TableDataSchema.CLOSE_FX].item()) - 1) * 100, 2)
        year_return = round(((data_complete.loc[yday_row, TableDataSchema.CLOSE_FX].item() / data_complete.loc[year_row, TableDataSchema.CLOSE_FX].item()) - 1) * 100, 2)

        yday_col.append(yday_return)
        mtd_col.append(mtd_return)
        ytd_col.append(ytd_return)
        year_col.append(year_return)

    df[TableSchema.DAY] = yday_col
    df[TableSchema.MTD] = mtd_col
    df[TableSchema.YTD] = ytd_col
    df[TableSchema.YEAR] = year_col

    return df

geo_table = table(geo_data_table_complete,
                  CategorySchema.GEO,
                  DateSchema.YESTERDAY,
                  DateSchema.MTD_START,
                  DateSchema.YTD_START,
                  DateSchema.YEAR_START)

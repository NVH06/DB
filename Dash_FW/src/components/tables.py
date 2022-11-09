from dash import Dash, html, dash_table
from dash.dependencies import Input, Output
import datetime
import calendar
from data.schemas import ids
from data.table_data import data_table_raw, data_table_complete, table, geo_table
from data.fx_data import fx_rate, fx_list
from data.schemas.data_id_schema import TickerSchema, CategorySchema
from data.schemas.input_schema import FXInputSchema

def render(app: Dash) -> html.Div():
    table_publish = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in geo_table.columns],
        data=geo_table.to_dict('records'),
        id=ids.GEO_TABLE)

    @app.callback(
        Output(ids.GEO_TABLE, "data"),
        Input(ids.TABLE_DATE_SELECTION, "date")
    )
    def update_table(date_sel) -> html.Div:
        END_DATE_SEL = datetime.datetime.strptime(date_sel, "%Y-%m-%d").date()
        print('END_DATE_SEL', END_DATE_SEL)

        if END_DATE_SEL.day == 1:
            lday_lmonth = calendar.monthrange(END_DATE_SEL.year, END_DATE_SEL.month - 2)[1]
            MTD_START = END_DATE_SEL.replace(month=END_DATE_SEL.month - 2, day=lday_lmonth)
        else:
            MTD_START = END_DATE_SEL.replace(day=1) - datetime.timedelta(days=1)

        if END_DATE_SEL.month == 1 and END_DATE_SEL.day == 1:
            YTD_START = END_DATE_SEL.replace(year=END_DATE_SEL.year - 2, month=12, day=31)
        else:
            YTD_START = END_DATE_SEL.replace(year=END_DATE_SEL.year - 1, month=12, day=31)

        print('MTD_START', MTD_START)
        YEAR_START = END_DATE_SEL.replace(year=END_DATE_SEL.year - 1)

        fx_rates = fx_rate(TickerSchema.FX, YEAR_START, END_DATE_SEL)
        geo_data_fx_list = fx_list(TickerSchema.GEO)

        geo_data_table_raw = data_table_raw(TickerSchema.GEO, YEAR_START,
                                            END_DATE_SEL)

        geo_data_table_complete = data_table_complete(geo_data_table_raw,
                                                      CategorySchema.GEO,
                                                      FXInputSchema.FX,
                                                      geo_data_fx_list,
                                                      fx_rates)

        geo_table_data = table(geo_data_table_complete,
                              CategorySchema.GEO,
                              END_DATE_SEL,
                              MTD_START,
                              YTD_START,
                              YEAR_START)

        return geo_table_data.to_dict('records')

    return html.Div(table_publish)

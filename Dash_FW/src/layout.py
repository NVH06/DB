from dash import Dash, html, dash_table
import pandas as pd
from data.schemas import ids
from data.schemas.df_schema import TableSchema
from data.table_data import geo_table
from src.components import chart_area_selection, chart, table_date_selection, tables

def create_layout(app: Dash) -> html.Div:
    df = geo_table

    return html.Div(
        className="ap-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(className="table-date-container", children=[table_date_selection.render(app)]),
            tables.render(app),
            chart.render(app),
            html.Div(className="checklist-container", children=[chart_area_selection.render(app)])
        ]
    )

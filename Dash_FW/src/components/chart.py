from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
from data.schemas import ids
from data import chart_data
from data.schemas.df_schema import GraphSchema

DATA = chart_data.geo_data_graph

def render(app: Dash) -> html.Div():
    @app.callback(
        Output(ids.YTD_GRAPH, "children"),
        Input(ids.AREA_CHECKLIST, "value")
    )
    def update_ytd_graph(areas) -> html.Div:
        # filtered_data = DATA.query("areas in @areas")
        mask = DATA[GraphSchema.CATEGORY].isin(areas)
        ytd_graph = px.line(
            DATA[mask],
            x=GraphSchema.DATE,
            y=GraphSchema.RETURN,
            color=GraphSchema.CATEGORY
        )
        return html.Div(dcc.Graph(figure=ytd_graph), id=ids.YTD_GRAPH)

    return html.Div(id=ids.YTD_GRAPH)

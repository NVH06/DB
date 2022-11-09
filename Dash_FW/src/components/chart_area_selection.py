from dash import Dash, html, dcc
from data.schemas import ids
from data.schemas.data_id_schema import CategorySchema

def render(app: Dash) -> html.Div:
    areas = CategorySchema.GEO
    return html.Div(
        children=[
            dcc.Checklist(
                id=ids.AREA_CHECKLIST,
                options=[{"label": area, "value": area} for area in areas],
                value=areas,
                inline=False
            )
        ]
    )
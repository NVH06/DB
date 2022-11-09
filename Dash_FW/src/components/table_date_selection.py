from dash import Dash, html, dcc
import datetime
from data.schemas import ids
from data.schemas.input_schema import DateSchema

def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            dcc.DatePickerSingle(
                id=ids.TABLE_DATE_SELECTION,
                min_date_allowed=DateSchema.YEAR_START,
                max_date_allowed=DateSchema.TODAY,
                initial_visible_month=DateSchema.TODAY,
                first_day_of_week=1,
                display_format="DD-MM-YYYY",
                date=DateSchema.TODAY
            )
        ]
    )
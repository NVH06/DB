class GraphSchema:
    DATE = 'Date'
    OPEN = 'Open'
    CLOSE = 'Close'
    FX = 'FX'
    FX_RATE = 'FX_Rate'
    OPEN_FX = 'Open_FX'
    CLOSE_FX = 'Close_FX'
    CATEGORY = 'Category'
    RETURNPCT = 'Return%'
    RETURN1 = 'Return_1'
    RETURN = 'Return(%)'

class TableDataSchema:
    DATE = 'Date'
    OPEN = 'Open'
    CLOSE = 'Close'
    FX = 'FX'
    FX_RATE = 'FX_Rate'
    OPEN_FX = 'Open_FX'
    CLOSE_FX = 'Close_FX'
    CATEGORY = 'Category'

class TableSchema:
    CATEGORY = 'Category'
    DAY = 'DAY%'
    MTD = 'MTD%'
    YTD = 'YTD%'
    YEAR = '1Y%'
    COLUMNS = [CATEGORY, DAY, MTD, YTD, YEAR]

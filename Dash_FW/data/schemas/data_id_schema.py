from data.schemas.input_schema import FXInputSchema

class TickerSchema:
    GEO = ['^GSPC', '^STOXX', '^FTSE', 'EEM', 'ACWI']

    if FXInputSchema.FX == 'EUR':
        FX = ['EURUSD=X', 'EURGBP=X']
    if FXInputSchema.FX == 'USD':
        FX = ['USDEUR=X', 'USDGBP=X']

class CategorySchema:
    GEO = ['US', 'Europe', 'UK', 'Emerging Markets', 'World']

    if FXInputSchema.FX == 'EUR':
        FX = ['EUR/USD', 'EUR/GBP']
    if FXInputSchema.FX == 'USD':
        FX = ['USD/EUR', 'USD/GBP']

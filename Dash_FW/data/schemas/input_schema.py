import datetime
import calendar

class DateSchema:
    TODAY = datetime.date.today()
    END_DATE_SEL = TODAY  # change to user input
    START_DATE_SEL = datetime.date(2021, 12, 31)  # change to user input
    YESTERDAY = END_DATE_SEL - datetime.timedelta(days=1)
    
    if YESTERDAY.day == 1:
        lday_lmonth = calendar.monthrange(YESTERDAY.year, YESTERDAY.month - 2)[1]
        MTD_START = YESTERDAY.replace(month=YESTERDAY.month - 2, day=lday_lmonth)
    else:
        MTD_START = YESTERDAY.replace(day=1) - datetime.timedelta(days=1)

    if YESTERDAY.month == 1 and YESTERDAY.day == 1:
        YTD_START = YESTERDAY.replace(year=YESTERDAY.year - 2, month=12, day=31)
    else:
        YTD_START = YESTERDAY.replace(year=YESTERDAY.year - 1, month=12, day=31)

    YEAR_START = YESTERDAY.replace(year=YESTERDAY.year-1)

class FXInputSchema:
    FX = 'EUR'  # change to user input

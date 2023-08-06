import locale
import time
from datetime import date, datetime


def decimal(val, decimal_places):
    """
    Format decimal values
    :param val: number
    :param decimal_places: number of decimal places
    :return: number
    """
    if isinstance(val, (int, float)):
        return round(val, decimal_places)
    return 0


def price(val):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(val, grouping=True, symbol=True)


def date_format(date_value: date):
    return date_value.strftime('%d/%m/%Y')


def date_time(dt_time: datetime):
    return dt_time.strftime('%d/%m/%Y %H:%M')


def date_time_integer(dt_time: datetime):
    return dt_time.strftime('%Y%m%d%H%M%S')


def to_date(day, month, year):
    try:
        return date(day=int(day), month=int(month), year=int(year))
    except Exception as error:
        raise RuntimeError(error)


def datetime_now_integer():
    return date_time_integer(datetime.now())


def to_time(str_time, pattern):
    return time.strptime(str_time, pattern)


def format_time(time_instance: time, pattern: str):
    return time.strftime(pattern, time_instance)

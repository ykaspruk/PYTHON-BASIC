"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
import datetime
from datetime import datetime, date, timedelta


class WrongFormatException(Exception):
    def __init__(self, date_string):
        self.date_string = date_string
        super().__init__(f"Date string '{date_string}' does not match format 'YYYY-MM-DD'.")


def calculate_days(from_date: str) -> int:
    today: date = date.today()
    try:
        from_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d")
        from_date_only: date = from_dt.date()
    except ValueError:
        raise WrongFormatException(from_date)

    date_difference: timedelta = today - from_date_only
    return date_difference.days
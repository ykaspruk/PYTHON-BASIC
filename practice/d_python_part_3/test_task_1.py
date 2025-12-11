"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""
import pytest
from datetime import datetime
from task_1 import WrongFormatException, calculate_days

TEST_TODAY = "2021-10-06"


def test_calculate_days_past_date(freezer):
    from_date = '2021-10-05'

    freezer.move_to(TEST_TODAY)

    today_dt = datetime.strptime(TEST_TODAY, "%Y-%m-%d").date()
    past_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
    expected_days = (today_dt - past_dt).days #  Expected: 1

    result = calculate_days(from_date)
    assert result == expected_days


@pytest.mark.freeze_time(TEST_TODAY)
def test_calculate_days_future_date():
    from_date = '2021-10-07'

    today_dt = datetime.strptime(TEST_TODAY, "%Y-%m-%d").date()
    future_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
    expected_days = (today_dt - future_dt).days  # Expected: -1

    result = calculate_days(from_date)
    assert result == expected_days


@pytest.mark.freeze_time(TEST_TODAY)
def test_calculate_days_same_day():
    from_date = '2021-10-06'
    expected_days = 0  # Difference: (Oct 6) - (Oct 6) = 0 days

    result = calculate_days(from_date)
    assert result == expected_days


@pytest.mark.freeze_time(TEST_TODAY)
def test_calculate_days_different_month_year():
    from_date = '2020-12-31'

    today_dt = datetime.strptime(TEST_TODAY, "%Y-%m-%d").date()
    past_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
    expected_days = (today_dt - past_dt).days

    result = calculate_days(from_date)
    assert result == expected_days


@pytest.mark.freeze_time(TEST_TODAY)
def test_calculate_days_invalid_format_exception():
    invalid_date = '10-07-2021'

    with pytest.raises(WrongFormatException) as excinfo:
        calculate_days(invalid_date)

    assert f"Date string '{invalid_date}' does not match format 'YYYY-MM-DD'." in str(excinfo.value)


@pytest.mark.freeze_time(TEST_TODAY)
def test_calculate_days_invalid_characters():
    invalid_string = 'not-a-date'

    with pytest.raises(WrongFormatException) as excinfo:
        calculate_days(invalid_string)

    assert f"Date string '{invalid_string}' does not match format 'YYYY-MM-DD'." in str(excinfo.value)

"""
Write tests for division() function in b_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

import pytest
from pathlib import Path
import sys

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
target_file_path = project_root / 'b_python_part_2'

if str(target_file_path) not in sys.path:
    sys.path.insert(0, str(target_file_path))

from task_exceptions import division


def test_division_ok(capfd):
    result = division(10, 2)

    assert result is None

    # Assert printed output using capfd
    out, err = capfd.readouterr()
    expected_output = "5\nDivision finished\n"
    assert out == expected_output

    division(10, 3)
    out, err = capfd.readouterr()
    expected_output = "3\nDivision finished\n"
    assert out == expected_output

    division(-10, 3)
    out, err = capfd.readouterr()
    expected_output = "-4\nDivision finished\n"
    assert out == expected_output


def test_division_by_zero(capfd):
    result = division(1, 0)

    assert result is None

    out, err = capfd.readouterr()
    expected_output = "Division by 0\nDivision finished\n"
    assert out == expected_output

    assert err == ""


def test_division_raises_exception(capfd):
    with pytest.raises(Exception) as excinfo:
        division(1, 1)

    assert "Deletion on 1 get the same result" in str(excinfo.value)

    out, err = capfd.readouterr()

    expected_output = "Division finished\n"
    assert out == expected_output
    assert err == ""
"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
from pathlib import Path
import sys

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
target_file_path = project_root / 'b_python_part_2'

if str(target_file_path) not in sys.path:
    sys.path.insert(0, str(target_file_path))

from task_input_output import read_numbers

FULL_MODULE_PATH = 'practice.b_python_part_2.task_input_output'


def test_read_numbers_without_text_input():
    N = 4
    mock_inputs = ['1', '2', '3', '4']

    expected_result = "Avg: 2.50"

    with patch('task_input_output.input', side_effect=mock_inputs):
        result = read_numbers(N)

    assert result == expected_result


def test_read_numbers_with_text_input():
    N = 3
    mock_inputs = ['1', '2', 'Text']

    expected_result = "Avg: 1.50"

    with patch('task_input_output.input', side_effect=mock_inputs):
        result = read_numbers(N)

    assert result == expected_result
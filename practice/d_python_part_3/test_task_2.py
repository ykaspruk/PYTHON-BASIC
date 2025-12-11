"""
Write tests for math_calculate function
"""
import pytest
from task_2 import math_calculate, OperationNotFoundException


def test_math_calculate_ceil_success():
    result = math_calculate('ceil', 10.7)
    assert result == 11


def test_math_calculate_floor_success():
    result = math_calculate('floor', 5.3)
    assert result == 5


def test_math_calculate_sqrt_success():
    result = math_calculate('sqrt', 81)
    assert result == 9.0


def test_math_calculate_log_success():
    result = math_calculate('log', 1024, 2)
    assert result == 10.0


def test_math_calculate_pow_success():
    result = math_calculate('pow', 2, 8)
    assert result == 256.0


def test_math_calculate_gcd_success():
    result = math_calculate('gcd', 48, 18)
    assert result == 6


def test_math_calculate_operation_not_found():
    with pytest.raises(OperationNotFoundException) as excinfo:
        math_calculate('non_existent_op', 1)

    assert "Operation 'non_existent_op' not found in the math module." in str(excinfo.value)


def test_math_calculate_no_arguments_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        math_calculate('ceil')

    assert "requires 1 or 2 arguments, but 0 were given." in str(excinfo.value)


def test_math_calculate_too_many_arguments_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        math_calculate('log', 10, 2, 5)

    assert "requires 1 or 2 arguments, but 3 were given." in str(excinfo.value)


def test_math_calculate_invalid_input_type():
    with pytest.raises(TypeError):
        math_calculate('sqrt', 'hello')
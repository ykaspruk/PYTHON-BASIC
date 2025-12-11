"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math


class OperationNotFoundException(Exception):
    def __init__(self, function_name):
        self.function_name = function_name
        super().__init__(f"Operation '{function_name}' not found in the math module.")


def math_calculate(function: str, *args):
    if not hasattr(math, function):
        raise OperationNotFoundException(function)

    math_func = getattr(math, function)

    arg_count = len(args)
    if arg_count not in (1, 2):
        raise TypeError(f"Function '{function}' requires 1 or 2 arguments, but {arg_count} were given.")

    try:
        return math_func(*args)
    except TypeError as e:
        raise TypeError(f"Error executing math function '{function}': {e}")
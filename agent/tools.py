from datetime import datetime


def get_current_time() -> str:
    """Return the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sum_numbers(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """Return the quotient of two numbers. Raises an error on division by zero."""
    if b == 0:
        raise ValueError("Division by zero is undefined.")
    return a / b


USER_TOOLS = [get_current_time, sum_numbers, subtract_numbers, multiply_numbers, divide_numbers]

BUILTIN_TOOLS = ["write_todos", "task", "ls", "read_file", "write_file", "edit_file", "glob", "grep"]

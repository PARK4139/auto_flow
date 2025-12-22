import logging
import traceback
from typing import Any

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def ensure_value_to_bool(value: Any) -> bool:
    """
    Converts a given value to a boolean.
    - If the value is already a boolean, it is returned as is.
    - If the value is a string, it returns True if the string is "true" (case-insensitive),
      and False if it is "false" (case-insensitive). Other strings raise a ValueError.
    - If the value is an integer, it returns True if it's non-zero, False otherwise.
    - Other types will attempt a standard bool() conversion, potentially raising a TypeError.

    Args:
        value (Any): The value to convert.

    Returns:
        bool: The boolean representation of the value.

    Raises:
        ValueError: If the input string is not "true" or "false".
        TypeError: For unsupported types or if standard bool() conversion fails.
    """
    try:
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            lower_value = value.lower()
            if lower_value == 'true':
                return True
            elif lower_value == 'false':
                return False
            else:
                raise ValueError(f"Cannot convert string '{value}' to boolean. Expected 'true' or 'false'.")
        elif isinstance(value, int):
            return bool(value)
        else:
            # Attempt standard bool() conversion for other types
            return bool(value)
    except Exception as e:
        logging.error(f"Error converting value '{value}' to boolean: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        raise # Re-raise the exception after logging

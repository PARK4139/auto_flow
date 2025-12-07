import sys
import clipboard
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from functools import partial
from fastapi import HTTPException

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_list_from_int_a_to_int_b(int_a: int, int_b: int) -> list[int]:
    step = 1 if int_b >= int_a else -1
    return list(range(int_a, int_b + step, step))

import logging
from enum import auto

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_texts import PkTexts


class PkMacros:
    PYCHARM_CODE_OPTIMIZATION = "PYCHARM_CODE_OPTIMIZATION" 

    _localized_texts = {
        "PYCHARM_CODE_OPTIMIZATION": {"kr": "PyCharm module script 최적화 매크로", "en": "Optimize PyCharm Code"}
    }


if __name__ == "__main__":
    import pyautogui
    from pk_internal_tools.pk_functions.ensure_refactoring_macro_executed import ensure_refactoring_macro_executed
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    # pk_*
    pyautogui.FAILSAFE = True

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

    try:
        func_n = get_caller_name()

        key_name = 'macro'
        options = [PkMacros.PYCHARM_CODE_OPTIMIZATION]
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
        macro = selected

        ensure_refactoring_macro_executed(macro)
    except Exception as e:
        ensure_debug_loged_verbose(traceback)

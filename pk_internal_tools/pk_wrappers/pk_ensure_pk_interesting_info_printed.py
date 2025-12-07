import traceback

from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging # Import logging for debug messages

if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_interesting_info_printed import ensure_pk_interesting_info_printed
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForGetPkInterestingInfo

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_pk_interesting_info_printed()

        ensure_console_paused()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
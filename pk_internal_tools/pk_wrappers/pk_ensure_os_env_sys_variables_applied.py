import os
import traceback

import ipdb

from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_os_env_sys_variables_applied import ensure_os_env_sys_variables_applied
from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

# from pk_external_tools.workspace.pk_workspace import ensure_this_code_operated

if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))
        ensure_os_env_sys_variables_applied()
        ensure_this_code_operated(ipdb)
        if QC_MODE:
            ensure_pk_log_editable(ipdb)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
#

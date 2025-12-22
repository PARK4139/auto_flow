import sys
from pathlib import Path
import traceback
import platform
import subprocess
import os 



from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

from auto_flow_internal_tools.functions.get_auto_flow_path import get_auto_flow_path
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


if __name__ == "__main__":
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))

        auto_flow_repo = get_auto_flow_path()
        system = platform.system()
        if system == "Windows":
            os.startfile(auto_flow_repo)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(auto_flow_repo)])
        else:  # Linux
            subprocess.run(["xdg-open", str(auto_flow_repo)])
        ensure_slept(milliseconds=2000)

    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)

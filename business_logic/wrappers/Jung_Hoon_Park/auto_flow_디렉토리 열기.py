import sys
from pathlib import Path
import traceback
import platform
import subprocess
import os 

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[3]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

from business_logic.functions.get_auto_flow_path import get_auto_flow_path
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
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

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

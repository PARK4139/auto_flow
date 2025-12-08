import sys
from pathlib import Path
import logging

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    logging.error("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_log_editable():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG

    # ensure_target_executed_2025_10_17_1649(editor=F_PYCHARM, target=F_PK_LOG, mode='a')
    # title = f"{get_nx(F_PK_LOG)} - Visual Studio Code"

    # ensure_target_executed_2025_10_17_1649(editor=F_VSCODE, target=F_PK_LOG, mode='a')
    # ensure_command_executed(cmd=f'start "" {F_PK_LOG}', mode='a')
    # ensure_command_executed(cmd=f'start "{get_nx(F_PK_LOG)}" explorer.exe {F_PK_LOG}') # 혹시 이게 닫히는 원인인가?
    # ensure_command_executed(cmd=f'start "{get_nx(F_PK_LOG)}" explorer.exe {F_PK_LOG}', mode='a')
    ensure_command_executed(cmd=f'start "{get_window_title_temp_identified(__file__)}" explorer.exe {F_PK_LOG}', mode='a')
    ensure_window_to_front(window_title_seg=get_nx(F_PK_LOG))
    # ensure_window_minimized(window_title=title)

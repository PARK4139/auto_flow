



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
import logging


def is_wsl_distro_started(wsl_distro_name):
    cmd = rf'wsl -l -v'
    # std_list = ensure_command_executed(cmd=cmd, encoding='utf-16')
    std_outs, std_errs = ensure_command_executed(cmd=cmd, encoding='utf-16-le')
    std_list = std_outs # Assign stdout_lines to std_list

    logging.debug(f"In is_wsl_distro_started, type(std_list)={type(std_list)}, std_list={std_list}")
    if std_list and len(std_list) > 0:
        logging.debug(f"In is_wsl_distro_started, type(std_list[0])={type(std_list[0])}, std_list[0]={std_list[0]}")
    try:
        from pk_internal_tools.pk_functions.get_list_removed_by_removing_runtine import get_list_removed_by_removing_runtine
    except ImportError:
        logging.error("Failed to import get_list_removed_by_removing_runtine. Please ensure the module is available.")
        return 0 # Or handle the error appropriately
    std_list = get_list_removed_by_removing_runtine(working_list=std_list)
    signature = wsl_distro_name
    signature2 = 'Running'
    for line in std_list:
        if signature in line:
            if signature2 in line:
                if QC_MODE:
                    logging.debug(f'''{wsl_distro_name} is started in wsl ''')
                return 1
    return 0

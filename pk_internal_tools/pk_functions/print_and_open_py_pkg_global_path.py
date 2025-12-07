from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_and_open_py_pkg_global_path():
    import sys

    for sys_path in sys.path:
        logging.debug(sys_path)
        if is_pattern_in_prompt(prompt=sys_path, pattern='site-packages') == True:
            logging.debug(f'''sys_path={sys_path}  ''')
            logging.debug(rf'echo "{sys_path}"')
            ensure_pnx_opened_by_ext(sys_path)


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging



def get_f_loading_nx_by_pattern(pattern):
    import re

    window_opened_list = get_windows_opened_with_hwnd()
    for window_opened in window_opened_list:
        match = re.search(pattern, window_opened)
        if match:
            f_loading_nx_matched = match.group(1)
            logging.debug(f'''f_loading_nx_matched={f_loading_nx_matched}  ''')
            return f_loading_nx_matched
        # else:
        #     logging.debug(f'''not matched  ''')

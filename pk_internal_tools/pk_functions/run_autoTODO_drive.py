

from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

import logging
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened


def run_autoTODO_drive():
    import time

    window_title_seg = "AutoTODO Drive"
    timeout = 5
    start_time = time.time()
    while 1:
        if time.time() - start_time > timeout:
            break
        if not is_window_opened(window_title_seg=window_title_seg):
            window_title_seg = "git log"
            os.chdir(rf"{D_HOME}\source\repos\ms_proto_drive")
            cmd = rf' start cmd.exe /k "title {window_title_seg}&& git log" '
            logging.debug(rf'''cmd="{cmd}"  ''')
            ensure_command_executed(cmd=cmd, mode="a")
            break
        ensure_slept(milliseconds=1000)

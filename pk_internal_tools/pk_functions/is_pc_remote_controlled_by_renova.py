import logging
import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_pk_screen_info import get_pk_screen_info
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def is_pc_remote_controlled_by_renova():
    try:
        info = get_pk_screen_info()
        if QC_MODE:
            logging.debug(info)

        # n. 모니터 개수가 1개인지 확인
        if info.count != 1:
            return False

        # n. 해당 모니터의 해상도가 1360x768인지 확인
        monitor = info.monitors[0]
        is_renova_resolution = (monitor.width == 1360 and monitor.height == 768)
        return is_renova_resolution
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return False

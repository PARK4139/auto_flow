import time

import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

@ensure_seconds_measured
def ensure_loop_trap_created():
    logging.debug("루프 트랩 인게이지")
    while 1:
        time.sleep(10)
        pass
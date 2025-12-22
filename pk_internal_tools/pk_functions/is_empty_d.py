

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_empty_d(d_src, debug_mode=True):
    import os
    import traceback

    try:
        if len(os.listdir(d_src)) == 0:
            return 1
        else:
            return 0
    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        return None

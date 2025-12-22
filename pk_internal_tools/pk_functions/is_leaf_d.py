from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.is_d import is_d
import logging


def is_leaf_d(d):
    import traceback

    import os
    logging.debug(f'''d={d}  ''')
    try:
        contents = os.listdir(d)
        if len(contents) > 0:
            return 0
        for content in contents:
            pnx = os.path.join(d, content)
            if is_d(pnx):
                return 0
        return 1
    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

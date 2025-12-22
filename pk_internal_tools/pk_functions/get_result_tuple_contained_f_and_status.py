from pathlib import Path
import logging
from pathlib import Path


def get_result_tuple_contained_f_and_status(d):
    import os

    d = Path(d)
    if is_d(d):
        result_tuple = {}
        for root, _, file_nxs in os.walk(d):
            for f_nx in file_nxs:
                f = os.path.join(root, f_nx)
                try:
                    if os.path.exists(f):
                        result_tuple[f] = os.path.getmtime(f)
                        # logging.debug(f'''result_tuple[f]={result_tuple[f]}  ''')
                    else:
                        logging.debug(f"f not found: {f}")
                except FileNotFoundError:
                    logging.debug(f"Error accessing file: {f}")
        return result_tuple
    return {}

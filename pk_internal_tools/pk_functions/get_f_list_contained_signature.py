from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_f_list_contained_signature(signature, d_pnx):
    import os
    if not os.path.exists(d_pnx):
        logging.debug(f'''Directory does not exist: {d_pnx}  ''')
        return None
    else:
        logging.debug(f'''Searching for signature="{signature}" in directory: {d_pnx}  ''')
    files_filtered = []
    for filename in os.listdir(d_pnx):
        if signature in filename:
            full_path = os.path.join(d_pnx, filename)
            logging.debug(f'''Found file: {full_path}  ''')
            files_filtered.append(full_path)
    else:
        logging.debug(f'''No file containing signature="{signature}" found in directory: {d_pnx}  ''')
    return files_filtered

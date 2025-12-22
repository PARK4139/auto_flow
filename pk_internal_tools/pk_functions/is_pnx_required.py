from pytube import Playlist

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_pnx_required(pnx):
    import os
    import string

    logging.debug(f'''pnx={pnx}  ''')
    if pnx == "":
        logging.debug(f'''pnx가 입력되지 않았습니다  ''')
        return 1
    connected_drives = []
    for drive_letter in string.ascii_uppercase:
        drive_path = drive_letter + ":\\"
        if os.path.exists(drive_path):
            connected_drives.append(drive_path)
            if pnx == drive_path:
                logging.debug(f'''입력된 pnx는 너무 광범위하여 진행할 수 없도록 설정되어 있습니다  ''')
                return 1
    if not os.path.exists(pnx):
        logging.debug(f'''입력된 pnx가 존재하지 않습니다  ''')
        return 1

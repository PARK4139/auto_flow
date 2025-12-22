from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
import logging
from pathlib import Path

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db


def save_to_f_and_get_video_list(f, d_working, allowed_extensions, file_name_parts_to_ignore):
    logging.debug(f'''f={f} ''')
    if not Path(f).exists():
        ensure_pnx_made(pnx=f, mode='f')
    v_f_list = get_files_filtered_from_db(d_working, allowed_extensions, file_name_parts_to_ignore)
    ensure_list_written_to_f(v_f_list, f, mode='w')
    return v_f_list

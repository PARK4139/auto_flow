def get_list_by_file_id(file_id, editable=False):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    import logging
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    import os
    import traceback
    f_historical = get_history_file_path(file_id)
    f = f_historical
    ensure_pnx_made(pnx=f_historical, mode='f')
    if editable == True:
        ensure_pnx_opened_by_ext(pnx=f_historical)
    logging.debug(f'''f={f}''')

    if f is None:
        return []

    try:
        if os.path.exists(f):
            with open(file=f, mode='r', encoding=PkEncoding.UTF8.value, errors='ignore') as f_obj:
                lines = f_obj.readlines()
                if lines is None:
                    return []
                return lines
    except:
        logging.debug(f'''{traceback.format_exc()}  " ''')



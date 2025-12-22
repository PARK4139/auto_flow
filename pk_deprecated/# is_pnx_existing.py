def is_pnx_existing(pnx=None, nx=None):
    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging
    from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
    from pk_internal_tools.pk_functions.get_d_working import get_d_working
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    if not pnx:
        if not nx:
            logging.warning(f'''{PkTexts.PNX_NX_ONLY_ONE_SET}. ''')
            ensure_paused()

    if pnx:
        path = Path(pnx)
        if path.exists():
            logging.debug(rf"{pnx} does exist")
            return True
        else:
            logging.debug(rf"{pnx} does not exist")
            return False

    if nx:
        # nx 기반 검색 로직 (기존 로직 유지)
        pnxs = get_pnxs(d_working=get_d_working(), with_walking=False)
        for path_str in pnxs:
            if nx in Path(path_str).name:
                logging.debug(rf"{pnx} does exist")
                return True
        logging.debug(rf"{pnx} does not exist")
        return False

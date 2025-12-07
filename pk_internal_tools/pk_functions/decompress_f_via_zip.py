def decompress_f_via_zip(f_decompressed):
    from pk_internal_tools.pk_functions.get_p import get_p
    import logging

    from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style

    import os
    import zipfile

    # cmd=rf'bz.exe x "{pnx}"'  # 화면에 창이 안뜨는 모드
    # ensure_command_executed(cmd=cmd)
    pnx_p = get_p(pnx=f_decompressed)
    if pnx_p is None:
        logging.warning(f"Failed to decompress {f_decompressed} from PNX")
        return None
    pnx_p = get_pnx_unix_style(pnx=pnx_p)
    f_decompressed = get_pnx_unix_style(pnx=f_decompressed)
    with zipfile.ZipFile(f_decompressed, 'r') as zip_ref:
        if not os.path.exists(pnx_p):
            os.makedirs(pnx_p)
        zip_ref.extractall(pnx_p)
    logging.debug(rf'''f_decompressed="{f_decompressed}"''')
    return f_decompressed

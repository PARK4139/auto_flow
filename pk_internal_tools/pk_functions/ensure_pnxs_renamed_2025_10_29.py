import logging

from pk_internal_tools.pk_functions.rename_pnx import rename_pnx

def ensure_pnxs_renamed_2025_10_29(pnx_list):
    import traceback

    for pnx in pnx_list:
        try:
            src = pnx[0]
            pnx_new = pnx[1]
            rename_pnx(src=src, pnx_new=pnx_new)
        except:
            logging.debug(f"{traceback.format_exc()}")

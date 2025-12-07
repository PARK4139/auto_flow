def ensure_pnx_moveds_without_overwrite(pnxs, dst):
    from pk_internal_tools.pk_functions.ensure_pnx_moved import ensure_pnx_moved

    for pnx in pnxs:
        ensure_pnx_moved(pnx=pnx, d_dst=dst)

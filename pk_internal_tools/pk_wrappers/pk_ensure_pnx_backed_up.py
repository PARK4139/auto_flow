if __name__ == "__main__":
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_directories import D_ARCHIVED, D_PK_MEMO_REPO
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_p import get_p
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        caller_n = get_caller_name()
        func_n = caller_n

        key_name = "pnx_working"
        options = [d_pk_root, D_PK_MEMO_REPO]
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=caller_n, options=options)
        pnx_working = selected

        key_name = "d_dst"
        options = [D_ARCHIVED]
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=caller_n, options=options)
        d_dst = selected

        # key_name = "blacklist"
        # options = [D_ARCHIVED, D_PK_RECYCLE_BIN, D_DESKTOP]
        # selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=caller_n, options=options)
        # blacklist = [selected]

        blacklist = []

        if QC_MODE:
            f_rar_new = ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=d_dst, blacklist=blacklist)
        else:
            f_rar_new = ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=d_dst, blacklist=blacklist)

        if f_rar_new:
            logging.debug(f'f_rar_new={f_rar_new}')
            logging.debug(f'get_p(f_rar_new)={get_p(f_rar_new)}')
            ensure_spoken(rf"압축성공")
            ensure_pnx_opened_by_ext(get_p(f_rar_new))
        else:
            logging.debug("f_rar_new is None, skipping ensure_pnx_opened_by_ext")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

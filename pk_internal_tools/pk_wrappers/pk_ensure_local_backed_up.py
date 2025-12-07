if __name__ == "__main__":
    import logging
    import traceback

    from pk_internal_tools.pk_functions import is_pnx_existing, ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_ARCHIVED, D_PK_MEMO_REPO
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        pnx_working = ensure_value_completed_2025_10_12_0000(key_name='pnx_working', options=[d_pk_root, D_PK_MEMO_REPO])

        # TODO : 동작검증 필요.
        # pk_option : 로컬백업 without .venv and .idea
        f = ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=D_ARCHIVED, with_timestamp=True)
        if not is_pnx_existing(f):
            logging.debug(f'''데일리 로컬백업 ''')
        elif is_pnx_existing(f):
            logging.debug(f'''데일리 로컬백업 ''')

        # pk_option : 로컬백업 all
        # if is_day(dd=15):
        #     f = ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=D_ARCHIVED)
        #     if not does_pnx_exist(f):
        #         logging.debug(f'''15일 전체 로컬백업 ''')
        #     elif does_pnx_exist(f):
        #         logging.debug(f'''15일 전체 로컬백업 ''')

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

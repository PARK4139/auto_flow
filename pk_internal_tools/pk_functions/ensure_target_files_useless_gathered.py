from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_target_files_useless_gathered():
    import logging
    import os
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.ensure_pnxs_move_to_recycle_bin import ensure_pnxs_move_to_recycle_bin
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
    from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
    from pk_internal_tools.pk_functions.is_empty_d import is_empty_d
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_WORKING
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_PK_RECYCLE_BIN
    from pk_internal_tools.pk_objects.pk_files import F_USELESS_FILE_NAMES_TXT

    try:

        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        d_working = None
        if QC_MODE:
            key_name = "d_working"
            file_to_working = get_file_id(key_name, func_n)
            historical_pnxs = get_historical_list(f=file_to_working)
            options = historical_pnxs + get_list_sorted(origins=[D_PK_WORKING, D_DOWNLOADS], mode_asc=True)
            d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=options)
            logging.debug(f'''len(historical_pnxs)={len(historical_pnxs)} ''')
            logging.debug(f'''len(options)={len(options)} ''')
            d_working = Path(d_working)
            values_to_save = [v for v in [d_working] + historical_pnxs + options if is_pnx_existing(pnx=v)]
            values_to_save = get_list_calculated(origin_list=values_to_save, dedup=True)
            ensure_list_written_to_f(f=file_to_working, working_list=values_to_save, mode="w")

        editable = True  # pk_option

        useless_file_names_txt = F_USELESS_FILE_NAMES_TXT
        if editable:
            ensure_pnx_opened_by_ext(pnx=useless_file_names_txt)

        dst = rf"{D_PK_RECYCLE_BIN}\pk_useless"
        ensure_pnx_made(pnx=dst, mode="d")
        logging.debug(f'''dst={dst}  ''')
        if not is_empty_d(d_src=dst):
            ensure_command_executed(cmd=rf'explorer "{dst}" ', encoding='cp949')

        os.chdir(d_working)

        # string_clipboard_bkp=get_text_from_clipboard()

        userless_files = set()
        useless_files = get_list_from_f(useless_file_names_txt)
        # open_pnx(pnx=useless_file_names_txt, debug_mode=True)
        for useless_f_nx in useless_files:
            if useless_f_nx is not None:
                useless_f_nx = useless_f_nx.strip()
                useless_f_nx = useless_f_nx.strip("\n")
                cmd = f'dir /b /s "{useless_f_nx}"'
                useless_files = ensure_command_executed(cmd=cmd, encoding='cp949')
                if useless_files is None:
                    useless_files = []
                for uleless_f in useless_files:
                    if is_pnx_existing(pnx=uleless_f):
                        userless_files.add(uleless_f)

        os.chdir(d_pk_root)
        if len(userless_files) == 0:
            logging.debug(f'''len(useless_f_set)={len(userless_files)}  ''')
            return
        else:
            for useless_f in userless_files:
                # ensure_pnx_moved(pnx=useless_f, d_dst=dst)  # todo : fix:외장드라이브에서는 안되는듯
                ensure_pnxs_move_to_recycle_bin(pnxs=[useless_f])
        logging.debug(rf'''dst="{dst}"  ''')
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)

if __name__ == "__main__":
    try:
        import traceback
        from pathlib import Path

        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
        from pk_internal_tools.pk_functions.ensure_target_files_gathered import ensure_target_files_gathered
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
        from pk_internal_tools.pk_functions.get_file_id import get_file_id
        from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
        from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
        from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_objects.pk_directories import d_pk_history, D_DOWNLOADS, D_PK_WORKING

        func_n = get_caller_name()

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

        while 1:
            key_name = "d_working"
            file_to_working = d_pk_history / f"{get_file_id(key_name, func_n)}.history"
            file_to_working = Path(file_to_working)
            historical_pnxs = get_historical_list(f=file_to_working)
            options = historical_pnxs + get_list_sorted(origins=[D_PK_WORKING, D_DOWNLOADS], mode_asc=True)
            if QC_MODE:
                d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=options)
            else:
                d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=options)
            values_to_save = [v for v in [d_working] + historical_pnxs + options if is_pnx_existing(pnx=v)]
            values_to_save = get_list_calculated(origin_list=values_to_save, dedup=True)
            ensure_list_written_to_f(f=file_to_working, working_list=values_to_save, mode="w")
            ensure_target_files_gathered(d_working)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

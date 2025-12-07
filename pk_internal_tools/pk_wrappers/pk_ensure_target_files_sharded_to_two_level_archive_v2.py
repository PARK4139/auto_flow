from pk_internal_tools.pk_functions import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_target_files_sharded_to_two_level_archive_v2 import ensure_target_files_sharded_to_two_level_archive_v2
from pk_internal_tools.pk_functions.get_drives_connected import get_drives_connected
from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_pk_log_initialized(__file__)
        ensure_window_title_replaced(get_nx(__file__))

        drive_selected = ensure_value_completed_2025_10_12_0000(key_name=rf"drive_selected", options=get_drives_connected())
        ensure_target_files_sharded_to_two_level_archive_v2(
            root_dir=drive_selected,
            # file_limit=300, # pk_option
            file_limit=76, # pk_option
            continue_on_error=False,
            db_path=F_pk_SQLITE,  # rf'{D_PK_DATA}/pk_system.sqlite'
            workers=1,  # PREVIEW에선 의미 없음
        )

        ensure_pk_wrapper_starter_suicided(__file__)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
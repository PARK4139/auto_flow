from pk_internal_tools.pk_functions.ensure_downloaded_videos_validated import ensure_downloaded_videos_validated
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADED_FROM_TORRENT, D_DOWNLOADS

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_PK_WORKING
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()

        options = [D_PK_WORKING, D_DOWNLOADED_FROM_TORRENT, D_DOWNLOADS]
        d_working = ensure_value_completed_2025_10_13_0000(key_name='d_working', options=options, func_n=func_n)
        ensure_downloaded_videos_validated(d_working=d_working)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_stand_output_stream_watched import ensure_stand_output_stream_watched
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()

        key_name = 'cmd'
        options = ["wsl -l -v"]
        cmd = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
        ensure_stand_output_stream_watched(cmd)  # TODO encoding 도 ensure_value_completed_2025_10_13_0000 받아야 할 가능성이 있어보인다.

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

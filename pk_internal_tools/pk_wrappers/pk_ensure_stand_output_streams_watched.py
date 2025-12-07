from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_stand_output_streams_watched import ensure_stand_output_streams_watched
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        func_n = get_caller_name()

        key_name = 'cmd1'
        options = ["wsl.exe -l -v"]
        cmd1 = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        key_name = 'cmd2'
        options = ["usbipd.exe list"]
        cmd2 = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        key_name = 'cmd3'
        options = ["wsl.exe lsusb"]
        cmd3 = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        key_name = 'milliseconds'
        options = [500, 1000, 2000, 5000, 10000]
        milliseconds = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
        milliseconds = int(milliseconds)


        cmds = [cmd1, cmd2, cmd3]
        ensure_stand_output_streams_watched(cmds, milliseconds=milliseconds)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

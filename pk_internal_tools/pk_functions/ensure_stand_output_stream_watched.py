# @ensure_seconds_measured
def ensure_stand_output_stream_watched(cmd, milliseconds=500, encoding=None):
    import logging
    import textwrap
    import traceback

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.get_str_dedented_from_list import get_str_dedented_from_list
    from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

    ensure_window_title_replaced(f"'{cmd}' watched")

    try:
        # pk_* -> watch command
        previous = None
        while True:
            stdouts, _ = ensure_command_executed(cmd, encoding=encoding, mode_silent=True)
            ensure_slept(milliseconds=milliseconds)
            if previous != stdouts:
                previous = stdouts
                ensure_console_cleared()
                # logging.debug(f'stdouts={stdouts}')
                # logging.debug(f'previous={previous}')
                title = textwrap.dedent(f"""
                    --- standard output stream watched like (watch -n {milliseconds / 1000} {cmd})---
                     
                """)
                stdouts = [title] + stdouts
                # pk_* -> get_str_dedented_from_list
                text_to_print = get_str_dedented_from_list(stdouts)

                logging.info(PK_UNDERLINE)
                logging.info(get_text_cyan(text_to_print))
    except KeyboardInterrupt:
        pass
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass

from pk_internal_tools.pk_functions.ensure_mail_found import ensure_mail_found

if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))

        # write code here
        # state =
        ensure_mail_found()
        ensure_pk_wrapper_starter_suicided(__file__) # pk_option
        # if state["state"]:
        #     ensure_pk_wrapper_starter_suicided(__file__) # pk_option

        # if QC_MODE:
        #     ensure_pk_log_editable(ipdb)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

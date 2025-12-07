if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_functions.replace_file_nxs_from_old_text_to_new_text import replace_file_nxs_from_old_text_to_new_text
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_objects.pk_directories import D_PK_OBJECTS

    try:
        ensure_pk_log_initialized(__file__=__file__)
        d_working = D_PK_OBJECTS
        old_text = 'pk_layer_100_'
        new_text = ''
        replace_file_nxs_from_old_text_to_new_text(d_working=d_working, old_text=old_text, new_text=new_text)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

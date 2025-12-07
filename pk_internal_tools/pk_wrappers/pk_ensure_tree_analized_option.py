if __name__ == '__main__':
    import traceback

    from pk_internal_tools.pk_functions.ensure_tree_analized_option import ensure_tree_analized_option
    from pk_internal_tools.pk_functions.ensure_chcp_65001 import ensure_chcp_65001
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
    

    try:

        if get_os_n() == 'windows':
            ensure_chcp_65001()

        while 1:
            ensure_tree_analized_option(d_src=rf"D:\pk_classifying")
            ensure_slept(hours=3)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

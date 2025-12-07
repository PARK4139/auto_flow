if __name__ == "__main__":
    try:
        from pk_internal_tools.pk_functions.ensure_todo_list_added import ensure_todo_list_added
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
        
        import traceback

        ensure_todo_list_added()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

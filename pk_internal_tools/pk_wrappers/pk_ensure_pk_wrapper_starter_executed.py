

if __name__ == "__main__":

    try:
        # By importing af_directory_paths, the project root is automatically
        # found and added to sys.path. This must be the first project import.
        import os
        import sys
        import traceback
        from af_internal_tools.constants import af_directory_paths
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed

        # Now we can use the centralized path
        d_pk_root = af_directory_paths.D_PROJECT_ROOT_PATH

    except Exception:
        traceback.print_exc()
        input("A critical error occurred during initial setup. Press Enter to exit...")
        sys.exit(1)

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        os.chdir(d_pk_root)
        ensure_pk_wrapper_starter_executed()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

if __name__ == "__main__":
    import sys
    from pathlib import Path
    import traceback

    # --- Start of embedded robust path setup ---
    # This logic must be embedded in any entry-point script to ensure
    # the project root is on sys.path before any project-internal imports.
    try:
        current_path = Path(__file__).resolve().parent
        project_root = None
        for parent in [current_path] + list(current_path.parents):
            if (parent / 'pyproject.toml').exists() or (parent / '.git').exists():
                project_root = parent
                break

        if project_root:
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
        else:
            # If root isn't found, we can't proceed with project imports.
            raise FileNotFoundError("Could not find project root from entry script.")
    except Exception as e:
        print(f"Critical error during path setup: {e}", file=sys.stderr)
        input("Press Enter to exit...")
        sys.exit(1)
    # --- End of embedded robust path setup ---

    # Now that the path is set, we can import project modules.
    try:
        # We can still use the centralized constants after the path is set.
        from af_internal_tools.constants import af_directory_paths
        
        import os
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed
        
        d_pk_root = af_directory_paths.D_PROJECT_ROOT_PATH

    except Exception:
        traceback.print_exc()
        # Using a raw input as a fallback if other modules failed to import
        input("A critical error occurred during module imports. Press Enter to exit...")
        sys.exit(1)

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        os.chdir(d_pk_root)
        ensure_pk_wrapper_starter_executed()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

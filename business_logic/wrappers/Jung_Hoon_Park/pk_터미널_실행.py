import sys
from pathlib import Path

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from pk_internal_tools.pk_functions.ensure_pk_terminal_executed import ensure_pk_terminal_executed

def main():
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        while True:
            ensure_pk_terminal_executed()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

if __name__ == "__main__":
    main()


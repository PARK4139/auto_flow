import traceback

from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
# Correctly import the interactive function from the 'functions' directory
from pk_internal_tools.pk_functions.ensure_target_files_classified_by_keyword import ensure_target_files_classified_by_keyword
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":
    """This wrapper serves as a simple entry point to the interactive classification function."""
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # The imported function now handles all user interaction.
        # No arguments are needed.
        ensure_target_files_classified_by_keyword()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

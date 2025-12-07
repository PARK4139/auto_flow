import traceback

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_todo_list_guided import ensure_todo_list_guided
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":
    try:
        ensure_todo_list_guided()


    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

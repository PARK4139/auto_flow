import sys
from pathlib import Path
import traceback



from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import d_pk_root


if __name__ == "__main__":
    try:
        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        ensure_window_title_replaced(get_nx(__file__))

        # 여기에 코드를 작성하세요.

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

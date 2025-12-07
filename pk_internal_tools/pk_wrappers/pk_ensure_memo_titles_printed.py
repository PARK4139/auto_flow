import traceback

from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_memo_titles_printed import ensure_memo_titles_printed
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_files import F_MEMO_RAW


try:
    ensure_pk_colorama_initialized_once()
    ensure_window_title_replaced(get_nx(__file__))
    f_memo = F_MEMO_RAW
    ensure_memo_titles_printed(f=f_memo)
     # pk_option
except Exception as exception:
    ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
finally:
    ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

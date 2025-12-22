import traceback

from auto_flow_internal_tools.functions.send_milling_data_L_CAM_to_LM_100 import send_milling_data_L_CAM_to_LM_100
from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import \
    ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import \
    ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

if __name__ == "__main__":
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))

        send_milling_data_L_CAM_to_LM_100()

    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)

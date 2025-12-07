import traceback

from pk_internal_tools.pk_objects.pk_wsl_controller import PkWslController
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        ptm = PkWslController()
        ptm.ensure_wsl_distro_assistance_executed()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

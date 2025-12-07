

import sys
import traceback

from colorama import init as pk_colorama_init

# from pk_internal_tools.pk_objects.500_live_logic import ensure_command_executed
#, '{PkTexts.TRY_GUIDE}', d_pk_system, '[ UNIT TEST EXCEPTION DISCOVERED ]'
#, print_red

ensure_pk_colorama_initialized_once()

if __name__ == "__main__":
    try:
        ensure_command_executed(cmd=f'sudo rm -rf {d_pk_system}/uv.lock')
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
        sys.exit(1)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
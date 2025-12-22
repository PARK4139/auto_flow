import logging
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT, D_ARCHIVED, D_PK_MEMO_REPO

if __name__ == "__main__":

    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()
        pnx_working = ensure_value_completed(
            key_name='pnx_working',
            options=[
                D_PK_ROOT,
                D_PK_MEMO_REPO
            ],
            func_n=func_n
        )

        # TODO : 동작검증 필요.
        # pk_option : 로컬백업 without .venv and .idea
        f = ensure_pnx_backed_up(pnx_working=pnx_working, d_destination=D_ARCHIVED, with_timestamp=True)
        if not Path(f).exists():
            logging.debug(f'''데일리 로컬백업 ''')
        elif Path(f).exists():
            logging.debug(f'''데일리 로컬백업 ''')

        # pk_option : 로컬백업 all
        # if is_day(dd=15):
        #     f = ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=D_ARCHIVED)
        #     if not does_pnx_exist(f):
        #         logging.debug(f'''15일 전체 로컬백업 ''')
        #     elif does_pnx_exist(f):
        #         logging.debug(f'''15일 전체 로컬백업 ''')

    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)

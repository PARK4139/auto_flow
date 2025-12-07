import logging

from pk_internal_tools.pk_functions.ensure_pk_interesting_infos_spoken import ensure_pk_interesting_infos_spoken
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForGetPkInterestingInfo

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_interesting_infos_printed import ensure_pk_interesting_infos_printed
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}모든 정보 음성 출력 (테스트){PK_ANSI_COLOR_MAP['RESET']}")
        ensure_pk_interesting_infos_spoken(flags=SetupOpsForGetPkInterestingInfo.ALL)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

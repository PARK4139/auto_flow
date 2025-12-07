# -*- coding: utf-8 -*-





if __name__ == '__main__':
    try:

        import traceback

        #  import ensure_chcp_65001
        #  import is_os_windows, get_f_current_n, pk_deprecated_get_d_current_n_like_human
        #, d_pk_system, '{PkTexts.TRY_GUIDE}', '[ DEBUGGING NOTE ]', '[ EXCEPTION DISCOVERED ]'
        # from pk_internal_tools.pk_objects.500_live_logic import assist_to_ensure_project_cmake_executed_at_remote_device_target
        #
        if is_os_windows():
            ensure_chcp_65001()
        assist_to_ensure_project_cmake_executed_at_remote_device_target()
        logging.debug(assist_to_ensure_project_cmake_executed_at_remote_device_target.__name__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
        d_current_n = pk_deprecated_get_d_current_n_like_human()
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
        traceback_format_exc_list = traceback.format_exc().split("\n")

        logging.debug(f'{PK_UNDERLINE}')
        for traceback_format_exc_str in traceback_format_exc_list:
            logging.debug(f'{'[ EXCEPTION DISCOVERED ]'} {traceback_format_exc_str}')
        logging.debug(f'{PK_UNDERLINE}')

        logging.debug(f'{PK_UNDERLINE}\n')
        logging.debug(f'{'[ DEBUGGING NOTE ]'} f_current={f_current_n}\nd_current={d_current_n}\n')
        logging.debug(f'{PK_UNDERLINE}\n')

        

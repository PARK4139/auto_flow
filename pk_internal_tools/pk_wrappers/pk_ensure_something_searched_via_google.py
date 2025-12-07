from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

if __name__ == "__main__":
    try:
        # todo
        while 1:
            should_i_search_to_google()
            print()
            print()
            print()
            print()

    except:
        f_current_n= get_f_current_n()
        d_current_n=get_d_current_n_like_human()
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
        traceback_format_exc_list = traceback.format_exc().split("\n")
        
        logging.debug(f'{PK_UNDERLINE}')
        for traceback_format_exc_str in traceback_format_exc_list:
            logging.debug(f'{STAMP_EXCEPTION_OCCURED} {traceback_format_exc_str}')
        logging.debug(f'{PK_UNDERLINE}')

        logging.debug(f'{PK_UNDERLINE}\n')
        logging.debug(f'{'[ DEBUGGING NOTE ]'} f_current={f_current_n}\nd_current={d_current_n}\n')
        logging.debug(f'{PK_UNDERLINE}\n')

        





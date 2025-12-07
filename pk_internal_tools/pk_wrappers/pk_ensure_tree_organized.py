# -*- coding: utf-8 -*-



if __name__ == '__main__':
    try:
        import traceback
        #  import deprecated_get_d_current_n_like_human, get_f_current_n, ensure_chcp_65001, get_os_n, ensure_tree_organized, gather_empty_d, get_p, organize_d_list_by_stamp
        # from pk_internal_tools.pk_objects.static_logic import d_pk_system, UNDERLINE, '{PkTexts.TRY_GUIDE}', '[ DEBUGGING NOTE ]', '[ EXCEPTION DISCOVERED ]', D_PK_WORKING
        #
        #
        import threading
        import time
        
        if get_os_n() == 'windows':
            ensure_chcp_65001()

        # [OPTION]
        # while 1:
        #     ensure_tree_organized(d_src=rf"D:\pk_classifying")
        #     sleep(hours=3)
        #     logging.debug(f'''wait for oraganize tree in loop %%%FOO%%%''')

        flag_to_detect_enter = 0

        def input_listener():
            global flag_to_detect_enter
            while 1:
                input()
                flag_to_detect_enter = 1


        def run_input_listener_loop():
            global flag_to_detect_enter

            # [OPTION]
            # d_working = rf"G:\Downloads"
            d_working = D_PK_WORKING

            # [OPTION]
            with_walking = True

            while 1:
                for _ in range(3 * 3600):  # 3시간 (3600초) 동안 1초씩 sleep
                    if flag_to_detect_enter:
                        flag_to_detect_enter = 0
                        logging.debug("Enter detected Restarting loop...")

                        ensure_tree_organized(d_working=d_working, with_walking=with_walking)
                        gather_empty_d(d_working=get_p(d_working))
                        # organize_d_list_by_stamp(d=get_p(d_working))
                        gather_empty_d(d_working=d_working)
                        organize_d_list_by_stamp(d=d_working)
                        logging.debug(f"wait for enter %%%FOO%%%")
                        break
                    time.sleep(1)

        # thread run ( in background )
        listener_thread = threading.Thread(target=input_listener, daemon=True)
        listener_thread.start()

        run_input_listener_loop()

    except Exception as e:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)

        logging.debug(f'{PK_UNDERLINE}')
        for traceback_format_exc_str in traceback_format_exc_list:
            logging.debug(f'{'[ EXCEPTION DISCOVERED ]'} {traceback_format_exc_str}')
        logging.debug(f'{PK_UNDERLINE}')

        

        

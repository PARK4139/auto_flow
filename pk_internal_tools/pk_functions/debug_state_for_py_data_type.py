def debug_state_for_py_data_type(pk_stamp, data_working, highlight_config_dict=None, with_QC_MODE=1):
    from pk_internal_tools.pk_functions.input_with_timeout import input_with_timeout
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import time
    if with_QC_MODE == 1:
        if QC_MODE == 1:
            if data_working:
                if isinstance(data_working, list):
                    for element in data_working:
                        # logging.debug(f'''element={element} ''')
                        logging.debug(element, highlight_config_dict)
                elif isinstance(data_working, dict):
                    for key, value in data_working.items():
                        logging.debug(f'{key}: {value}', highlight_config_dict)
                elif isinstance(data_working, str):
                    logging.debug(f'{data_working}', highlight_config_dict)

            pk_time_limit = 30
            pk_time_s = time.time()
            while 1:
                elapsed = time.time() - pk_time_s
                if elapsed >= pk_time_limit:
                    logging.debug(f'''time out (pk_time_limit={pk_time_limit}) ''')
                    break
                user_input = input_with_timeout(
                    text_working=rf'[?] [?] Press Enter to continue.',
                    timeout_secs=int(pk_time_limit - elapsed))
                if not user_input:
                    user_input = ""
                if user_input == "":
                    break
    elif with_QC_MODE == 0:  # QC_MODE=0 이더라도 출력은 그대로 쓸때
        if data_working:
            if isinstance(data_working, list):
                for element in data_working:
                    logging.debug(element, highlight_config_dict)
            elif isinstance(data_working, dict):
                for key, value in data_working.items():
                    logging.debug(f'{key}: {value}', highlight_config_dict)
            elif isinstance(data_working, str):
                logging.debug(f'{data_working}', highlight_config_dict)

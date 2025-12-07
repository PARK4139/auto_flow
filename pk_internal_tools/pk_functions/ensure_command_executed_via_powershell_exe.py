def ensure_command_executed_via_powershell_exe(cmd, console_keep_mode=False, admin_mode=False):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    import logging
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_str_from_clipboard import get_str_from_clipboard
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_functions.run_powershell_exe import run_powershell_exe
    from pk_internal_tools.pk_functions.run_powershell_exe_as_admin import run_powershell_exe_as_admin
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import time

    # | clip 을 하여도 값을 읽어오기 어려운 경우가 있음
    window_title_seg = rf'PowerShell'
    logging.debug(rf'''cmd="{cmd}"  ''')
    if not is_window_opened(window_title_seg=window_title_seg):
        # run_cmd_exe()
        if admin_mode == False:
            window_title_seg = rf'powershell'
            run_powershell_exe()
        else:
            window_title_seg = rf'PowerShell'
            run_powershell_exe_as_admin()
    ensure_window_to_front(window_title_seg)

    std_output_stream = ""
    time_limit = 5
    time_s = time.time()
    while 1:
        if ensure_window_to_front(window_title_seg):
            # ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(string=rf"cd {wsl_pnx} | xclip -sel clip", mode="wsl") # fail: cd는 xclip 으로 pipe 할 수 없음
            ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text=cmd)
            ensure_pressed("enter")
            std_output_stream = get_str_from_clipboard()
            break
        # 5초가 지났는지 확인
        # logging.debug(time.time() - time_s)
        if time.time() - time_s > time_limit:
            logging.debug("5 seconds passed. Exiting loop.")
            break
        ensure_slept(seconds=0.5)  # CPU 점유율을 낮추기 위해 약간의 대기

    if console_keep_mode == False:
        time_limit = 5
        time_s = time.time()
        while 1:
            if ensure_window_to_front(window_title_seg):
                ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text="exit")
                ensure_pressed("enter")
                if admin_mode == False:
                    ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text="exit")
                    ensure_pressed("enter")
                break
            # logging.debug(time.time() - time_s)
            if time.time() - time_s > time_limit:
                logging.debug("5 seconds passed. Exiting loop.")
                break
            ensure_slept(seconds=0.5)  # CPU 점유율을 낮추기 위해 약간의 대기
    return std_output_stream

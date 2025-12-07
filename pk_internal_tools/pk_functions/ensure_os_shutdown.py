import logging


def ensure_os_shutdown():
    from pk_internal_tools.pk_functions.ensure_gemini_cli_killed import ensure_gemini_cli_killed
    from pk_internal_tools.pk_functions.ensure_losslescut_killed import ensure_losslescut_killed

    from pk_internal_tools.pk_functions.ensure_cmd_exe_killed import ensure_cmd_exe_killed
    from pk_internal_tools.pk_functions.ensure_potplayer_killed import ensure_potplayer_killed
    from pk_internal_tools.pk_functions.ensure_process_killed_by_image_name import ensure_process_killed_by_image_name

    ensure_potplayer_killed()
    ensure_losslescut_killed()
    ensure_process_killed_by_image_name('chrome.exe')
    ensure_process_killed_by_image_name('code.exe')
    ensure_process_killed_by_image_name('cursor.exe')
    ensure_gemini_cli_killed()
    ensure_cmd_exe_killed()

    # seconds = ensure_value_completed_2025_10_12_0000(key_hint='seconds=', values=[5,10])
    # if seconds == "":
    #     seconds = 1
    # seconds = int(seconds)
    seconds = 5
    logging.debug(rf"seconds={seconds}")
    ensure_os_shutdown_v2(seconds)


def ensure_os_shutdown_v1():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    ensure_command_executed(rf'%windir%\System32\Shutdown.exe -s ')


def ensure_os_shutdown_v2(seconds=None, milliseconds=None, mins=None, restart_mode=0, cancel_mode=0):
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    import logging
    mode_list = [restart_mode, cancel_mode]
    false_count = mode_list.count(False)

    none_list = [seconds, milliseconds, mins]
    none_count = none_list.count(None)

    if false_count == 2 and none_count == 3:
        logging.debug(f"이 함수의 최소인자의 수는 1개 입니다")
        return

    if false_count < 2:
        if restart_mode == 1:
            cmd = f'shutdown.exe /r'
            ensure_command_executed(cmd=cmd)
            return

        if cancel_mode == 1:
            cmd = f'shutdown.exe /a'
            ensure_command_executed(cmd=cmd)
            return
    else:

        if none_count != 2:
            logging.debug(f"이 함수는 시간단위에 대한인자를 1개의 인자만 받도록 만들어졌습니다")
            return

        # sys_shutdown(seconds=x)
        # sys_shutdown(mins=x)
        if milliseconds is not None:
            seconds = milliseconds
        elif mins is not None:
            seconds = mins * 60

        ensure_command_executed(cmd=f'shutdown.exe /s /t {seconds}')

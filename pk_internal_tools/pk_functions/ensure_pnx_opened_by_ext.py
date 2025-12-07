def ensure_pnx_opened_by_ext(pnx):
    import logging
    import time
    import os

    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_objects.pk_files import f_pycharm64_exe
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    try:
        logging.debug(rf"pnx={pnx}")
        if pnx is None:
            logging.debug("파일 경로가 None입니다. 파일을 열 수 없습니다.")
            return

        pnx = str(pnx)

        # TODO : fzf 로 opener 설정
        if is_os_windows():

            x = os.path.splitext(pnx)[1].lower().replace('.', '')
            opener = None
            ext_to_program = None
            if get_os_n() == 'windows':
                ext_to_program = {
                    '': ('explorer.exe', 'directory, opening in windows explorer'),
                    # 'log': (f'{F_VSCODE_LNK}', 'log file, opening in VS Code'),
                    'log': (f'{f_pycharm64_exe}', 'log file, opening in VS Code'),
                    'py': (str(f_pycharm64_exe), 'python file, opening in PyCharm'),
                    'bat': (str(f_pycharm64_exe), 'batch file, opening in PyCharm'),
                }
            program_to_open, description = ext_to_program.get(x, (None, None))
            if program_to_open:
                opener = program_to_open
                pnx = get_pnx_windows_style(pnx=pnx)
                logging.debug(f"ensure_pnx_opened_by_ext: {pnx} is a {description}")

            # text_editor가 None이면 os.startfile() 시도
            if opener is None:
                try:
                    os.startfile(pnx)
                    logging.debug(f"'{pnx}' 파일을 시스템 기본 프로그램으로 열었습니다.")
                except OSError as e:
                    logging.error(f"'{pnx}' 파일을 열 수 없습니다: {e}. 확장자 '{x}'에 대한 기본 프로그램이 설정되지 않았을 수 있습니다.")
                    logging.debug("파일을 수동으로 열거나, 해당 확장자에 대한 기본 프로그램을 설정해주세요.")
            else:
                # text_editor가 설정된 경우, 기존 ensure_command_executed 로직 사용
                cmd = f'"{opener}" "{pnx}"'
                ensure_command_executed(cmd=cmd, mode='a')

                # pk_* -> timeout_seconds_limit loop
                timeout_seconds_limit = 3
                time_s = time.time()
                while True:
                    if time.time() - time_s > timeout_seconds_limit:
                        logging.debug("timeout")
                        break
                    if is_window_opened(window_title_seg=pnx):
                        break
                    ensure_slept(milliseconds=10)

        else:
            try:
                from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
                ensure_not_prepared_yet_guided()
            except ImportError:
                # fallback: 간단한 메시지 출력
                print("Linux 환경에서는 파일 열기 기능이 아직 구현되지 않았습니다.")
            # if x == '':  # d 인 경우
            #     text_editor = 'explorer.exe'
            # elif x == 'txt':
            #     text_editor = 'gedit' # nvim, nano, vim, code
            # # elif x == 'csv':
            # #     text_editor = 'explorer.exe'
            # # elif x == 'xlsx':
            # #     text_editor = 'explorer.exe'
            # # elif x == 'xls':
            # #     text_editor = 'explorer.exe'
            # pnx = get_pnx_unix_style(pnx=pnx)
    except:
        logging.debug("❌ An unexpected error occurred")

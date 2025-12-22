

from selenium.webdriver.common.by import By
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pathlib import Path


def run_and_login_acu_update_v3_exe_and_run_autoTODOdrive_release_exe(issue_log_index_data):
    import os.path

    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    AUTOTODODRIVE_RELEASE_SW_VERSION_EXE = rf"{D_HOME}\Desktop\AutoA2zDrive\AutoTODODrive_Release_{issue_log_index_data["SW 버전"]}.exe"
    logging.debug(
        text_working=rf'''AUTOTODODRIVE_RELEASE_SW_VERSION_EXE="{AUTOTODODRIVE_RELEASE_SW_VERSION_EXE}"  ''')
    window_title_seg = "acu_update_v3_exe"
    if not Path(AUTOTODODRIVE_RELEASE_SW_VERSION_EXE).exists():
        acu_update_v3_exe = rf"{D_HOME}\Desktop\AutoA2zDrive\ACU_update_v3.exe"
        acu_update_v3_exe_p = get_p(pnx=acu_update_v3_exe)
        os.chdir(acu_update_v3_exe_p)
        cmd = rf' start cmd.exe /k "title {window_title_seg}&& {D_HOME}\Desktop\AutoA2zDrive\ACU_update_v3.exe &" '
        ensure_command_executed(cmd=cmd, mode="a")
        pw = get_token_from_f_token(f_token=rf'{D_PK_RECYCLE_BIN}\token_linux_pw.txt', initial_str="")
        user_n = get_token_from_f_token(f_token=rf'{D_PK_RECYCLE_BIN}\token_linux_id.txt', initial_str="")
        while 1:
            ensure_slept(milliseconds=2000)
            if is_window_opened(window_title_seg=window_title_seg):
                ensure_window_to_front(window_title_seg)
                ensure_slept(milliseconds=500)
                ensure_writen_like_human(text_working=user_n)
                ensure_pressed("enter")
                ensure_writen_like_human(text_working=pw)
                ensure_pressed("enter")
                ensure_writen_like_human("2")
                ensure_pressed("enter")
                ensure_writen_like_human(rf"{issue_log_index_data["SW 버전"]}")
                ensure_pressed("enter")
                break
    else:
        run_autoTODOdrive_release_exe()

from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
import logging
from pathlib import Path


def run_f_n_as_script():  # todo : chore : add parameter

    f_p = rf'{D_PK_EXTERNAL_TOOLS}'
    f_n = 'pk_ensure_chrome_youtube_cookies_saved_to_file'
    f_pn_py = Path(rf"{f_p}/{f_n}.py")
    f_pn_cmd = rf"{D_PK_EXTERNAL_TOOLS}\{f_n}.cmd"
    activate_bat = rf'{D_PK_ROOT}\.venv\Scripts\activate.cmd'
    python_exe = rf'{D_PK_ROOT}\.venv\Scripts\python.exe'
    CRLF = '%%%CRLF%%%'
    script_str = rf'''
       :: @echo off{CRLF}
       chcp 65001 >NUL{CRLF}
       title %~nx0{CRLF}   
       cls{CRLF}

       :: 관리자 권한 요청{CRLF}
       :: net session >NUL 2>&1{CRLF}
       :: if %errorLevel% neq 0 ({CRLF}
       ::     powershell -Command "Start-Process python -ArgumentList '\"%~dp0myscript.py\"' -Verb RunAs"{CRLF}
       ::     exit /b{CRLF}
       :: ){CRLF}
       :: cls{CRLF}

       call "{activate_bat}"{CRLF}
       set PYTHONPATH={D_PK_ROOT}{CRLF}
       "{python_exe}" "{f_pn_py}"{CRLF}
     '''
    script_list = script_str.split(CRLF)
    script_list = get_list_replaced_element_from_str_to_str(working_list=script_list, from_str='    ', to_str='')
    ensure_pnx_made(pnx=f_pn_cmd, mode='f', script_list=script_list)
    logging.debug(rf"set PYTHONPATH={D_PK_ROOT}")
    # ensure_command_executed(cmd=rf'notepad "{activate_bat}"')
    # ensure_command_executed(cmd=rf'notepad "{f_pn_cmd}"')
    ensure_command_executed(cmd=rf'start call "{f_pn_cmd}" ', encoding=PkEncoding.UTF8, mode='a')

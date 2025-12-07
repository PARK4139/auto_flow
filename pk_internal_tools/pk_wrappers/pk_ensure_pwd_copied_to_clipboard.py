from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
import logging
from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts


import traceback

from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
import ipdb

from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))

        pwd = get_pwd_in_python()
        logging.debug(f'''pwd={pwd} ''')

        # OS별 클립보드 복사 처리
        if is_os_windows():
            ensure_text_saved_to_clipboard(pwd)
        elif is_os_linux():
            # Linux에서는 xclip 또는 xsel 사용
            try:
                import subprocess
                subprocess.run(['xclip', '-selection', 'clipboard'], input=pwd.encode(), check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(['xsel', '--clipboard'], input=pwd.encode(), check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # 클립보드 도구가 없으면 출력만
                    logging.debug(f"{PkTexts.CLIPBOARD_COPY_FAILED}. {PkTexts.PATH}: {pwd}")
        else:
            # macOS에서는 pbcopy 사용
            try:
                import subprocess
                subprocess.run(['pbcopy'], input=pwd.encode(), check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logging.debug(f"{PkTexts.CLIPBOARD_COPY_FAILED}. {PkTexts.PATH}: {pwd}")

        ensure_pk_wrapper_starter_suicided(__file__) # pk_option

        if QC_MODE:
            ensure_pk_log_editable(ipdb)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)


import yt_dlp
import re

from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def download_pnx_to_git_v3(d_working, git_repo_url, commit_msg, branch_n):
    import traceback
    import threading
    import time
    # from colorama import init as pk_colorama_init

    # ensure_pk_colorama_initialized_once()

    def ask_user_yes_no(msg, timeout=10):
        logging.debug(f"{msg} (y/n, {timeout}초 내 응답): ")
        result = {'answer': None}

        def _get_input():
            try:
                result['answer'] = input().strip().lower()
            except Exception:
                result['answer'] = None

        def _countdown():
            for seconds in reversed(range(1, timeout + 1)):
                logging.debug(f"[{PkTexts.TIME_LEFT}] [hours:minute:seconds] [{seconds}{PkTexts.SECONDS}]")
                time.sleep(1)

        input_thread = threading.Thread(target=_get_input)
        timer_thread = threading.Thread(target=_countdown)
        input_thread.daemon = True
        timer_thread.daemon = True
        input_thread.start()
        timer_thread.start()

        input_thread.join(timeout)

        if result['answer'] is None:
            logging.debug(f"{PkTexts.RESPONSE_TIMEOUT}.")
            return 0

        return result['answer'] == 'y'

    try:
        if not is_pnx_existing(pnx=d_working):
            ensure_pnx_made(pnx=d_working, mode='d')

        d_git = rf"{d_working}/.git"

        if not is_pnx_existing(pnx=d_git):
            std_list = ensure_command_executed(f'git clone -b {branch_n} {git_repo_url} {d_working}')
            debug_state_for_py_data_type('%%%CLONE%%%', std_list)

            if any("fatal:" in line.lower() for line in std_list):
                logging.debug(f"{PkTexts.GIT_CLONE_FAILED}: {std_list}")
                return
        else:
            os.chdir(d_working)
            std_list = ensure_command_executed(f'git pull origin {branch_n}')
            debug_state_for_py_data_type('%%%PULL%%%', std_list)

            if any("couldn't find remote ref" in line.lower() for line in std_list):
                logging.debug(f"브랜치 '{branch_n}' 이(가) 원격 레포지토리에 없습니다.")
                if ask_user_yes_no(f"브랜치 '{branch_n}' 를 새로 만드시겠습니까?"):
                    std_list = ensure_command_executed(f'git checkout -b {branch_n}')
                    debug_state_for_py_data_type('%%%CHECKOUT_NEW_BRANCH%%%', std_list)

                    std_list = ensure_command_executed(f'git push -u origin {branch_n}')
                    debug_state_for_py_data_type('%%%PUSH_NEW_BRANCH%%%', std_list)

                    if any("error:" in line.lower() or "failed to push" in line.lower() for line in std_list):
                        logging.debug(f"{PkTexts.BRANCH_PUSH_FAILED}: {std_list}")

                        if ask_user_yes_no("커밋이 없어서 푸시에 실패한 것 같습니다. 빈 커밋을 생성할까요?"):
                            std_list = ensure_command_executed('git commit --allow-empty -m "init empty commit"')
                            debug_state_for_py_data_type('%%%EMPTY_COMMIT%%%', std_list)

                            std_list = ensure_command_executed(f'git push -u origin {branch_n}')
                            debug_state_for_py_data_type('%%%PUSH_AFTER_EMPTY_COMMIT%%%', std_list)

                            if any("error:" in line.lower() or "failed to push" in line.lower() for line in std_list):
                                logging.debug(f"{PkTexts.EMPTY_COMMIT_PUSH_FAILED}: {std_list}")
                                return
                        else:
                            logging.debug(f"{PkTexts.USER_CANCELLED_EMPTY_COMMIT}.")
                            return
                else:
                    logging.debug(f"{PkTexts.USER_CANCELLED_BRANCH_CREATION}.")
                    return
            elif any("fatal:" in line.lower() for line in std_list):
                logging.debug(f"{PkTexts.GIT_PULL_FAILED}: {std_list}")
                return

        logging.debug(f"{PkTexts.GIT_WORK_COMPLETE}: {d_working} ")

    except Exception:
        logging.debug(f"{traceback.format_exc()} ")

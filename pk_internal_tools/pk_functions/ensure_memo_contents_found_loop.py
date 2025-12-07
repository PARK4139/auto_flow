from pk_internal_tools.pk_functions import ensure_console_cleared
from pk_internal_tools.pk_functions.ensure_memo_contents_found import ensure_memo_contents_found
from pk_internal_tools.pk_functions.ensure_pk_exit_silent import ensure_pk_exit_silent


def ensure_memo_contents_found_loop():
    loop_cnt = 1
    user_input = None
    while True:
        if loop_cnt == 1:
            loop_cnt += 1
        else:
            user_input = input("\n계속 검색하려면 Enter, 종료하려면 'x' 입력: ").strip().lower()
            loop_cnt += 1
        if user_input in ("q", "quit", "exit", "x"):
            logging.debug("검색 반복을 종료합니다.")
            ensure_pk_exit_silent()
            break
        try:
            ensure_console_cleared()
            ensure_memo_contents_found()
        except Exception as e:
            logging.debug(f"검색 중 오류 발생: {e}")

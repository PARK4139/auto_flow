from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_target_executed_2025_10_17_1649 import ensure_target_executed_2025_10_17_1649


@ensure_seconds_measured
def ensure_chatgpt_opened():
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_objects.pk_urls import URL_CHATGPT_PK_WORKING
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    # ensure_target_executed_2025_10_17_1649("explorer.exe", URL_CHATGPT_PK_WORKING)
    ensure_command_executed( get_text_chain("explorer.exe", URL_CHATGPT_PK_WORKING))


    # TODO : naver,  google, nyasii  URL tab 으로  고를때는 nickname,   맵으로 나오도록
    # 아침코딩이 오히려 즐겁다.
    # gtts 내가 고치자.

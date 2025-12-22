# def ensure_value_completed_legacy(key_hint, options):

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def _print_guide_text():
    import textwrap

    import logging

    from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    # pk_* -> guide simple
    guide_text = textwrap.dedent(rf'''
        # {PkTexts.ANSWER} SHORTCUT
        list options:tab
        select option:Enter
        select other:arrow key
        free writting:typing
        
                    ''')
    logging.debug(get_text_cyan(guide_text))

def ensure_value_completed_2025_10_12_0000(key_name, options):
    """
    TODO : ensure_value_completed_2025_10_12_0000 함수에서 간헐적으로 tab 키로 자동완성이 안되는 이슈가 있음.
    """
    import logging
    from pathlib import Path

    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
    from prompt_toolkit.history import InMemoryHistory

    from pk_internal_tools.pk_objects.pk_texts import PK_BLANK
    from pk_internal_tools.pk_functions.ensure_pk_exit_silent import ensure_pk_exit_silent
    from pk_internal_tools.pk_functions.is_path_like import is_path_like
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    seen = set()
    deduped = []
    options = options + [PkTexts.SHUTDOWN]

    for option in options:
        # None 값은 건너뛰기
        if option is None:
            continue

        # 모든 타입을 안전하게 문자열로 변환
        try:
            if isinstance(option, Path):
                styled = str(option)
            elif isinstance(option, str):
                if is_path_like(option):
                    styled = Path(option)
                else:
                    styled = option
            else:
                # 기타 타입도 문자열로 변환
                styled = str(option)

            # styled가 여전히 Path 객체인 경우 추가 변환
            if hasattr(styled, 'lower') and callable(getattr(styled, 'lower')):
                # styled가 lower() 메서드를 가진 객체인 경우 (문자열 등)
                pass
            else:
                # styled가 lower() 메서드를 가지지 않은 객체인 경우 (Path 등)
                styled = str(styled)

        except Exception as e:
            # 변환 중 오류가 발생하면 문자열로 강제 변환
            logging.warning(f"Option conversion failed: {option} -> {e}")
            styled = str(option)

        if styled not in seen:
            seen.add(styled)
            deduped.append(styled)

    # fzf 스타일 실시간 검색 완성 기능 유지
    completer = FuzzyCompleter(WordCompleter(deduped, ignore_case=True))

    if QC_MODE:
        # _print_guide_text()
        pass
    else:
        # TODO {PkTexts.ANSWER} {PkTexts.GUIDE} 미출력 설정 옵션, 종료 옵션과 함께 추가하도록 설정
        _print_guide_text()

    key_name = key_name.replace('?', ' ')


    message = rf"{key_name}={PK_BLANK}"
    # ensure_spoken(rf"{get_easy_speakable_text(message)} 를 입력해주세요")

    # -> 간헐적 자동완성 fail->
    # ensure_slept(milliseconds=444)
    # import sys, asyncio
    # if sys.platform.startswith('win'):
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    option_selected = prompt(
        message=message,
        completer=completer,
        history=InMemoryHistory(),  # 빈 history 사용으로 자동입력 방지
        complete_in_thread=False,  # 백그라운드 완성 비활성화
        complete_while_typing=False,  # 타이핑 중 자동완성 비활성화
        enable_history_search=False,  # history 검색 비활성화
        mouse_support=False,  # 마우스 지원 비활성화
        multiline=False,  # 단일 라인 입력만 허용
        enable_suspend=False,  # suspend 기능 비활성화
        enable_open_in_editor=False,  # 에디터 열기 비활성화
        # complete_style="default",      # 기본 자동완성 스타일 유지
    )

    if option_selected.strip() == PkTexts.SHUTDOWN:
        ensure_pk_exit_silent()
        return
    return option_selected

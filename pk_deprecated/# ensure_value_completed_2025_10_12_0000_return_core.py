from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_value_completed_return_core(message, options):
    import logging

    from pathlib import Path

    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter, FuzzyCompleter

    from pk_internal_tools.pk_functions.ensure_pk_exit_silent import ensure_pk_exit_silent
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.is_path_like import is_path_like
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if message.strip() == "x":
        ensure_spoken(f"{func_n}() exited(intended)")
        return None

    seen = set()
    deduped = []
    options = options + [PkTexts.SHUTDOWN]
    for option in options:
        # None 값은 건너뛰기
        if option is None:
            continue
        styled = option
        if isinstance(option, str):
            if is_path_like(option):
                styled = Path(option)
        if styled not in seen:
            seen.add(styled)
            deduped.append(styled)

    # fzf 스타일 실시간 검색 완성 기능 유지
    completer = FuzzyCompleter(WordCompleter(deduped, ignore_case=True))

    # 원본 상태로 복원 - 기본 prompt_toolkit 사용
    option_selected = prompt(
        message + " ",
        completer=completer,
    )

    if option_selected.strip() == PkTexts.SHUTDOWN:
        logging.debug("??")
        ensure_pk_exit_silent()
        return
    return option_selected

from functools import cache

from pk_internal_tools.pk_functions.get_gemini_cli_window_title_by_manual import get_gemini_cli_window_title_by_manual


# @ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
@cache  # 프로그램 실행 1회만 실행, 캐시하여 값 반환.
def get_gemini_cli_window_title():
    import logging

    from pk_internal_tools.pk_functions.get_gemini_cli_expected_titles import get_gemini_cli_expected_titles
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title_by_auto import get_gemini_cli_window_title_by_auto

    options = get_gemini_cli_expected_titles()
    logging.debug(f"Options for window title search: {options}")

    # way 2 : auto
    gemini_cli_window_title = get_gemini_cli_window_title_by_auto(gemini_cli_titles=options)
    if gemini_cli_window_title:
        return gemini_cli_window_title

    # way 1 : manual (fallback)
    gemini_cli_window_title = get_gemini_cli_window_title_by_manual(options)
    if gemini_cli_window_title:
        return gemini_cli_window_title

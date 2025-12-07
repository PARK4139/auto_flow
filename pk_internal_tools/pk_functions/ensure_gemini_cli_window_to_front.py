from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


# @ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
@ensure_pk_ttl_cached(ttl_seconds=30 * 1 * 1, maxsize=10)
def get_gemini_cli_window_title_cached():
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    return get_gemini_cli_window_title()


def ensure_gemini_cli_window_to_front():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    from pk_internal_tools.pk_functions.get_pk_tts_cache_file_play_length_milliseconds import get_pk_tts_cache_file_play_length_milliseconds
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened

    # gemini_cli_window_title = get_gemini_cli_window_title_cached()
    gemini_cli_window_title = get_gemini_cli_window_title()
    text1 = None
    text2 = None
    for window_title in get_windows_opened():
        if window_title == gemini_cli_window_title:
            ensure_window_to_front(gemini_cli_window_title)
            ensure_window_resized_and_positioned_left_half()
            text1 = f"{window_title}를 앞으로 이동 시도하였습니다."
            text1 = get_easy_speakable_text(text1)
            ensure_spoken(text1)
    else:
        text2 = f"{gemini_cli_window_title}를 앞으로 이동할 창이 없었습니다"
        text2 = get_easy_speakable_text(text2)
        ensure_spoken(text2)
        pass

    # milliseconds = get_pk_tts_cache_file_play_length_milliseconds(text1)  + get_pk_tts_cache_file_play_length_milliseconds(text2)
    milliseconds = get_pk_tts_cache_file_play_length_milliseconds(text2)
    ensure_slept(milliseconds=milliseconds)

    # pk_*
    ensure_spoken(wait=True)

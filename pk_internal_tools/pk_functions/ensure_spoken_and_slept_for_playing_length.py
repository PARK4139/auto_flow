from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_spoken_and_slept_for_playing_length(text):
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_pk_tts_cache_file_play_length_milliseconds import get_pk_tts_cache_file_play_length_milliseconds

    ensure_spoken(text)
    ensure_slept(milliseconds=get_pk_tts_cache_file_play_length_milliseconds(text))

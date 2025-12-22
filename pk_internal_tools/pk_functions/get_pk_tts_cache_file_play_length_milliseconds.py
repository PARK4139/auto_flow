
import logging

def get_pk_tts_cache_file_play_length_milliseconds(text: str, language: str = "ko") -> int | None:
    """
    Retrieves the playback length of a cached TTS audio file in milliseconds.
    Returns None if the file is not found or its duration cannot be determined.
    """
    try:
        from mutagen.mp3 import MP3, MutagenError
        from pk_internal_tools.pk_objects import pk_tts_cache_utils
    except ImportError as e:
        logging.error(f"get_pk_tts_cache_file_play_length_milliseconds: Failed to import necessary modules: {e}")
        return None

    from .ensure_split_text_for_tts import ensure_split_text_for_tts

    total_duration_milliseconds = 0
    phrases = ensure_split_text_for_tts(text)

    if not phrases:
        logging.warning(f"No valid phrases found after splitting text: '{text}'")
        return 0 # Or None, depending on desired behavior for empty phrases

    for phrase in phrases:
        audio_path = pk_tts_cache_utils.find_existing_cache_path(phrase, language)

        if not audio_path:
            logging.warning(f"Cached audio file not found for phrase: '{phrase[:30]}...'")
            continue # Skip this phrase, contribute 0 to total

        try:
            audio = MP3(audio_path)
            duration_seconds = audio.info.length
            duration_milliseconds = int(duration_seconds * 1000)
            logging.debug(f"Found audio duration for '{phrase[:30]}...': {duration_milliseconds}ms")
            total_duration_milliseconds += duration_milliseconds
        except MutagenError:
            logging.error(f"Failed to read metadata from audio file: {audio_path}. It might be corrupted. Skipping phrase.")
            continue
        except Exception as e:
            logging.error(f"An unexpected error occurred for phrase '{phrase[:30]}...' in get_pk_tts_cache_file_play_length_milliseconds: {e}. Skipping phrase.")
            continue
    
    logging.debug(f"Total audio duration for '{text[:30]}...': {total_duration_milliseconds}ms")
    return total_duration_milliseconds

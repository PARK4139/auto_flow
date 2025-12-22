from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_spoken import get_pk_spoken_manager


@ensure_seconds_measured
def ensure_spoken_legacy(text, after_delay=1.00, delimiter=None, voice_config=None, speed_factor=1.30, verbose=False):
    import logging

    from pk_internal_tools.pk_objects.pk_spoken_manager import VoiceConfig

    logging.debug(f"Input text: '{text}'")
    if verbose:
        logging.debug(f"Delimiter: '{delimiter}'")
        logging.debug(f"Voice config: {voice_config}")

    try:
        pk_spoken_manager = get_pk_spoken_manager()

        if voice_config:
            # Assuming voice_config is a dictionary that can be used to create a VoiceConfig object
            if isinstance(voice_config, dict):
                config = VoiceConfig(**voice_config)
                pk_spoken_manager.set_voice_config(config)
            elif isinstance(voice_config, VoiceConfig):
                pk_spoken_manager.set_voice_config(voice_config)

        if delimiter and delimiter in text:
            segments = [seg.strip() for seg in text.split(delimiter) if seg.strip()]
            if verbose:
                logging.debug(f"Detected delimiter '{delimiter}'")
                logging.debug(f"Number of segments: {len(segments)}")

            for i, seg in enumerate(segments):
                if verbose:
                    logging.debug(f"Speaking segment {i + 1}: '{seg}'")
                pk_spoken_manager.speak(seg)
        else:
            if verbose:
                logging.debug("Single text processing mode")
            pk_spoken_manager.speak(text)
        return True
    except Exception as e:
        if verbose:
            import traceback
            logging.debug(f"TTS Error: {e}")
            logging.debug(f"Traceback:\n{traceback.format_exc()}")
        return False

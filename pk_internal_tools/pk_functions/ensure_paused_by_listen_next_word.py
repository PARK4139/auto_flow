# pk_internal_tools/pk_functions/ensure_paused_by_listen_next_word.py
# -*- coding: utf-8 -*-
import logging
import traceback
from textwrap import dedent

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def ensure_paused_by_listen_next_word(text_to_listen: str = "next") -> None:
    """Pauses execution until a specific text is spoken.

    This function listens for microphone input and waits until the specified
    text (defaulting to "next") is detected. It is designed to
    halt a process and wait for a voice command to continue.

    Args:
        text_to_listen (str, optional): The text to listen for to stop pausing.
                                   Defaults to "next".

    Returns:
        None
    """
    # Lazy import for performance and avoiding circular dependencies
    try:
        import speech_recognition as sr
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    except ImportError:
        logging.error(
            "SpeechRecognition library not found. "
            "Please install it with 'uv pip install SpeechRecognition PyAudio'."
        )
        return

    r = sr.Recognizer()
    mic = sr.Microphone()

    logging.info(f"Waiting until '{text_to_listen}' is spoken...")
    with mic as source:
        # r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        while True:
            try:
                logging.debug("Waiting for voice input...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                logging.debug("Recognizing voice...")
                recognized_text = r.recognize_google(audio, language='en-US')
                logging.info(f"Recognized text: {recognized_text}")

                if text_to_listen in recognized_text:
                    logging.info(f"'{text_to_listen}' detected. Continuing execution.")
                    break
                else:
                    logging.debug(f"'{text_to_listen}' not found. Waiting again.")

            except sr.UnknownValueError:
                logging.warning("Could not understand audio. Retrying.")
            except sr.RequestError as e:
                error_message = f"Could not request results from Google Speech Recognition service; {e}"
                logging.error(error_message)
                ensure_debugged_verbose(traceback=traceback, e=e)
                # In case of network error, it might be better to break the loop
                # or implement a retry-limit. For now, we'll break.
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                ensure_debugged_verbose(traceback=traceback, e=e)
                break

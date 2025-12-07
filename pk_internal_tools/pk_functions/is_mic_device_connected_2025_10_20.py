def is_mic_device_connected_2025_10_20():
    """
    Checks for microphone availability using the SpeechRecognition library,
    avoiding a direct dependency on PyAudio.
    """
    import speech_recognition as sr
    import logging
    
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if mic_list:
            logging.debug(f"Microphones found: {mic_list}")
            return 1  # True, microphones are available
        else:
            logging.debug("No microphones found.")
            return 0  # False, no microphones found
    except Exception as e:
        # The library might raise an exception if no audio backend is found at all
        logging.error(f"An error occurred while checking for microphones: {e}")
        return 0 # False

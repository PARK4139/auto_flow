


def ensure_parrot_executed():
    import logging
    import traceback
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    while 1:
        try:
            logging.debug("말씀해주세요")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            str_prompt = recognizer.recognize_google(audio, language="ko")
            logging.debug_and_speak(rf"{str_prompt}")
        except sr.UnknownValueError:
            pass
        except OSError:
            logging.debug(f'''마이크 장비가 없습니다" ''')
            break
        except Exception as e:
            logging.debug(f'''"음성 인식 서비스에 오류가 발생했습니다"" ''')
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

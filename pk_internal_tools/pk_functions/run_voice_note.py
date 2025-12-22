from tkinter import UNDERLINE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pathlib import Path

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging



def run_voice_note():
    import traceback
    import speech_recognition as sr

    from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
    f_txt = D_PK_CONFIG / "voice_memo.txt"

    f_txt = get_pnx_unix_style(pnx=f_txt)
    if not Path(f_txt).exists():
        ensure_pnx_made(pnx=f_txt, mode='f')

    ensure_str_writen_to_f(msg=f"{PK_UNDERLINE}{get_pk_time_2025_10_20_1159('now')}\n", f=f_txt)

    f_txt = get_pnx_windows_style(pnx=f_txt)
    cmd = rf"explorer {f_txt}"
    ensure_command_executed(cmd=cmd, mode='a')

    logging.debug_and_speak("저는 텍스트f에 받아쓰는 음성메모장 voice_note 입니다")
    recognizer = sr.Recognizer()

    while 1:
        try:
            logging.debug_and_speak("말씀해주세요")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            str_prompt = recognizer.recognize_google(audio, language="ko")
            logging.debug_and_speak(rf"{str_prompt}")

            # 텍스트를 f에 저장
            with open(file=f_txt, mode="a", encoding=PkEncoding.UTF8.value) as file:
                file.write(str_prompt + "\n")
        except sr.UnknownValueError:
            pass  # 음성을 인식하지 못한 경우 무시
        except OSError:
            logging.debug(f'''마이크 장비가 없습니다" ''')
            break
        except Exception as e:
            logging.debug(f'''"음성 인식 서비스에 오류가 발생했습니다"" ''')
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

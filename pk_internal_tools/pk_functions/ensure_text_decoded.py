from pk_internal_tools.pk_functions.get_master_pw import get_master_pw
from pk_internal_tools.pk_functions.get_text_decoded import get_text_decoded
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def ensure_text_decoded():
    # 암호화 복호화 모듈은 실패 케이스 만 로깅
    import logging
    import pyperclip

    text = input("text_encoded=").strip()

    if not text:
        logging.debug("복호화할 텍스트가 입력되지 않았습니다.")
        return None

    master_password = get_master_pw()
    logging.debug(f'''master_password={master_password} ''')

    # n. get_text_decoded 함수를 사용하여 텍스트 복호화
    try:
        text_decoded = get_text_decoded(text, master_password)

        if text_decoded is None:
            logging.debug("복호화에 실패했습니다. 텍스트 형식과 패스워드를 확인하세요.")
            return None

        try:
            pyperclip.copy(text_decoded)
        except Exception as e:
            logging.debug(f"️ 클립보드 복사 실패: {str(e)}")

        text_plain = text_decoded
        return text_plain

    except Exception as e:
        logging.debug(f"복호화 중 오류 발생: {str(e)}")
        return None

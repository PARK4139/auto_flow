import os
import logging
import logging
from datetime import datetime

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_objects.pk_texts import PkTexts

def ensure_directory_made_at_pwd() -> str:
    options = [
        "pk_test",
        "pk_temp",
        "pk_working_s",
        "pk_working_ani",
        "archive_" + datetime.now().strftime('%Y%m%d'),
    ]

    # 사용자 입력 받기
    dir_name = ensure_value_completed(
        key_name="dir_name=",
        options=options
    ).strip()

    # 입력 없으면 타임스탬프 기반 이름 생성
    if not dir_name:
        dir_name = f"dir_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    pwd = os.getcwd()
    full_path = os.path.join(pwd, dir_name)

    try:
        os.makedirs(full_path, exist_ok=True)
        logging.debug(f"[{PkTexts.CREATED}] DIRECTORY : {full_path}")
    except Exception as e:
        logging.error(f"[{PkTexts.ERROR}] Failed to create directory: {e}")
        raise

    return full_path

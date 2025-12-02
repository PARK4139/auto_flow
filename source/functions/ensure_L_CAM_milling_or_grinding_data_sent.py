import sys
import traceback
import os
import logging
from pathlib import Path

from pk_system.pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_system.pk_internal_tools.pk_functions.get_caller_name import get_caller_name


def ensure_L_CAM_milling_or_grinding_data_sent(
    data_file_path=None,
    recipient_email=None,
    subject=None,
    body=None
):
    """
    L-CAM 밀링 또는 그라인딩 데이터를 전송합니다.
    
    Args:
        data_file_path: 전송할 데이터 파일 경로
        recipient_email: 수신자 이메일 주소. None이면 환경 변수에서 가져옴
        subject: 이메일 제목
        body: 이메일 본문
    """
    try:
        func_n = get_caller_name()
        logging.info(f"{func_n}: L-CAM 데이터 전송 시작")
        
        # 기본값 설정
        if data_file_path is None:
            logging.warning("데이터 파일 경로가 제공되지 않았습니다.")
            return False
        
        data_file_path = Path(data_file_path)
        
        if not data_file_path.exists():
            logging.error(f"데이터 파일을 찾을 수 없습니다: {data_file_path}")
            return False
        
        # 환경 변수에서 수신자 이메일 가져오기
        if recipient_email is None:
            recipient_email = os.getenv("L_CAM_RECIPIENT_EMAIL", "")
            if not recipient_email:
                raise ValueError("L_CAM_RECIPIENT_EMAIL 환경 변수가 설정되지 않았습니다. .env 파일에 L_CAM_RECIPIENT_EMAIL을 설정해주세요.")
        
        if subject is None:
            subject = f"L-CAM 데이터 전송 - {data_file_path.name}"
        
        if body is None:
            body = f"L-CAM 밀링/그라인딩 데이터 파일을 첨부합니다.\n\n파일명: {data_file_path.name}"
        
        # 이메일 클라이언트를 통한 전송 (mailto: 링크 사용)
        import urllib.parse
        mailto_url = f"mailto:{recipient_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        
        import webbrowser
        webbrowser.open(mailto_url)
        ensure_slept(milliseconds=1000)
        
        # 파일을 첨부하기 위해 클립보드에 파일 경로 복사 (수동 첨부 필요)
        from pk_system.pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
        ensure_text_saved_to_clipboard(str(data_file_path))
        
        logging.info(f"{func_n}: 이메일 클라이언트가 열렸습니다. 파일 경로가 클립보드에 복사되었습니다.")
        logging.info(f"{func_n}: 수동으로 파일을 첨부해주세요.")
        
        return True
        
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return False

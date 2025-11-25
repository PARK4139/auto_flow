import sys
import traceback
import os
import webbrowser
from pathlib import Path

from pk_system.pk_sources.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_sources.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_system.pk_sources.pk_functions.get_windows_opened import get_windows_opened
from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept


def ensure_huvitz_mail_opened(mail_url=None):
    """
    Huvitz 메일을 엽니다 (웹 메일 또는 메일 클라이언트).
    
    Args:
        mail_url: 메일 URL. None이면 환경 변수에서 가져옴
    """
    try:
        # 환경 변수에서 메일 URL 가져오기
        if mail_url is None:
            mail_url = os.getenv("HUVITZ_MAIL_URL", "")
            if not mail_url:
                raise ValueError("HUVITZ_MAIL_URL 환경 변수가 설정되지 않았습니다. .env 파일에 HUVITZ_MAIL_URL을 설정해주세요.")
        
        # 이미 열려있는 메일 창이 있는지 확인
        windows = get_windows_opened()
        mail_window_found = False
        for window in windows:
            window_lower = window.lower()
            if "mail" in window_lower or "huvitz" in window_lower or "outlook" in window_lower:
                mail_window_found = True
                ensure_window_to_front(window)
                ensure_slept(milliseconds=500)
                break
        
        # 창이 없으면 새로 열기
        if not mail_window_found:
            webbrowser.open(mail_url)
            ensure_slept(milliseconds=1000)  # 브라우저가 열릴 때까지 대기
            # 열린 창에 포커스
            ensure_slept(milliseconds=500)
            windows = get_windows_opened()
            for window in windows:
                window_lower = window.lower()
                if "mail" in window_lower or "huvitz" in window_lower or "chrome" in window_lower or "edge" in window_lower:
                    ensure_window_to_front(window)
                    break
        
    except Exception:
        ensure_debug_loged_verbose(traceback)


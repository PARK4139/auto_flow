import sys
import traceback
import os
import webbrowser
from pathlib import Path

from pk_system.pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_system.pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_system.pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def ensure_ehr_login(ehr_url=None):
    """
    EHR 로그인 페이지를 열고 포커스를 맞춥니다.
    
    Args:
        ehr_url: EHR 로그인 URL. None이면 환경 변수에서 가져옴
    """
    try:
        # 환경 변수에서 EHR URL 가져오기
        if ehr_url is None:
            ehr_url = os.getenv("EHR_URL", "")
            if not ehr_url:
                raise ValueError("EHR_URL 환경 변수가 설정되지 않았습니다. .env 파일에 EHR_URL을 설정해주세요.")
        
        # 이미 열려있는 EHR 창이 있는지 확인
        windows = get_windows_opened()
        ehr_window_found = False
        for window in windows:
            if "ehr" in window.lower() or "huvitz" in window.lower():
                ehr_window_found = True
                ensure_window_to_front(window)
                ensure_slept(milliseconds=500)
                break
        
        # 창이 없으면 새로 열기
        if not ehr_window_found:
            webbrowser.open(ehr_url)
            ensure_slept(milliseconds=1000)  # 브라우저가 열릴 때까지 대기
            # 열린 창에 포커스
            ensure_slept(milliseconds=500)
            windows = get_windows_opened()
            for window in windows:
                if "ehr" in window.lower() or "huvitz" in window.lower() or "chrome" in window.lower() or "edge" in window.lower():
                    ensure_window_to_front(window)
                    break
        
    except Exception:
        ensure_debug_loged_verbose(traceback)


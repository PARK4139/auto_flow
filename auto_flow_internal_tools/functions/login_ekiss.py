import sys
import traceback
import os
import webbrowser
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def ensure_ekiss_login(driver=None, ekiss_url=None):
    """
    eKiss 로그인 페이지를 열고 포커스를 맞춥니다.
    Selenium driver가 제공되면 해당 드라이버를 사용하여 페이지를 엽니다.
    
    Args:
        driver: Selenium WebDriver 객체 (옵션)
        ekiss_url: eKiss 로그인 URL. None이면 환경 변수에서 가져옴
    """
    try:
        # 환경 변수에서 eKiss URL 가져오기
        if ekiss_url is None:
            ekiss_url = os.getenv("EKISS_URL", "")
            if not ekiss_url:
                raise ValueError("EKISS_URL 환경 변수가 설정되지 않았습니다. .env 파일에 EKISS_URL을 설정해주세요.")

        if driver:
            driver.get(ekiss_url)
            print(f"Selenium 드라이버를 사용하여 {ekiss_url}로 이동했습니다.")
            # Selenium 사용 시 창 핸들은 driver에서 관리하므로 window focus 로직은 불필요할 수 있음
            # driver.maximize_window() # 필요 시 창 최대화
            return

        # --- Selenium 드라이버가 없을 경우 기존 로직 ---
        # 이미 열려있는 eKiss 창이 있는지 확인
        windows = get_windows_opened()
        ekiss_window_found = False
        for window in windows:
            if "ekiss" in window.lower() or "kiss" in window.lower():
                ekiss_window_found = True
                ensure_window_to_front(window)
                ensure_slept(milliseconds=500)
                break
        
        # 창이 없으면 새로 열기
        if not ekiss_window_found:
            webbrowser.open(ekiss_url)
            ensure_slept(milliseconds=1000)  # 브라우저가 열릴 때까지 대기
            # 열린 창에 포커스
            ensure_slept(milliseconds=500)
            windows = get_windows_opened()
            for window in windows:
                if "ekiss" in window.lower() or "kiss" in window.lower() or "chrome" in window.lower() or "edge" in window.lower():
                    ensure_window_to_front(window)
                    break
        
    except Exception as e:
        ensure_debugged_verbose(traceback, e)


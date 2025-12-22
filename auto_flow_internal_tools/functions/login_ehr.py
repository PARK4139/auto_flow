import sys
import traceback
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

def ensure_ehr_login(driver, ehr_url=None, ehr_id=None, ehr_pw=None):
    """
    EHR 로그인 페이지를 열고 자동으로 로그인합니다.
    Selenium driver가 제공되어야 합니다.
    
    Args:
        driver: Selenium WebDriver 객체
        ehr_url: EHR 로그인 URL. None이면 환경 변수에서 가져옴
        ehr_id: EHR 아이디. None이면 환경 변수에서 가져옴
        ehr_pw: EHR 비밀번호. None이면 환경 변수에서 가져옴
    """
    try:
        # 환경 변수에서 정보 가져오기
        if ehr_url is None:
            ehr_url = os.getenv("EHR_URL")
            if not ehr_url:
                raise ValueError("EHR_URL 환경 변수가 설정되지 않았습니다.")
        if ehr_id is None:
            ehr_id = os.getenv("EHR_ID")
            if not ehr_id:
                raise ValueError("EHR_ID 환경 변수가 설정되지 않았습니다.")
        if ehr_pw is None:
            ehr_pw = os.getenv("EHR_PW")
            if not ehr_pw:
                raise ValueError("EHR_PW 환경 변수가 설정되지 않았습니다.")

        # EHR 페이지로 이동
        driver.get(ehr_url)
        print(f"EHR 로그인 페이지로 이동: {ehr_url}")

        wait = WebDriverWait(driver, 10)

        # ID/PW 입력 및 로그인
        # 아래 ID는 실제 EHR 페이지의 HTML 요소 ID에 맞게 수정해야 합니다.
        id_field = wait.until(EC.presence_of_element_located((By.ID, "user_id"))) # pk_option
        pw_field = driver.find_element(By.ID, "user_pw") # pk_option
        login_button = driver.find_element(By.ID, "login_btn") # pk_option

        id_field.send_keys(ehr_id)
        pw_field.send_keys(ehr_pw)
        
        ensure_slept(milliseconds=500)
        login_button.click()

        print("EHR 로그인을 시도합니다.")

    except Exception as e:
        ensure_debugged_verbose(traceback, e)

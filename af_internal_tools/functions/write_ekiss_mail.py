
import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from af_internal_tools.functions.login_ehr import ensure_ehr_login
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def write_ekiss_mail():
    """
    eKiss에 로그인하고 메일 쓰기 페이지로 이동합니다.
    """
    driver = None
    try:
        # Selenium WebDriver 설정
        driver = None
        try:
            # 기존에 열린 크롬에 연결 시도 (디버깅 포트 사용)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            driver = webdriver.Chrome(options=chrome_options)
            
            # 현재 URL이 ekiss인지 확인
            if "ekiss.huvitz.com" not in driver.current_url:
                ensure_ehr_login(driver)

        except Exception:
            # 새로운 드라이버 시작
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            ensure_ehr_login(driver)

        wait = WebDriverWait(driver, 10)

        while True:
            ensure_slept(milliseconds=1000)
            if "main.aspx" in driver.current_url:
                # 메일 아이콘 클릭
                mail_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "go_email()")]')))
                mail_link.click()

                # 메일 페이지(iframe)로 전환될 때까지 대기
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mail_body")))

                # 메일쓰기 버튼 클릭
                compose_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "#compose")]')))
                compose_button.click()
                
                print("eKiss 메일 쓰기 페이지로 이동했습니다.")
                
                # 작업 완료 후 루프 탈출
                break
            else:
                print("메인 페이지로 이동을 기다립니다...")


    except Exception:
        ensure_debug_loged_verbose(traceback)
    finally:
        # 이 스크립트에서 드라이버를 새로 시작했다면 종료
        # 기존 브라우저에 연결했다면 그대로 둠
        # 이 부분은 프로젝트의 드라이버 관리 정책에 따라 달라져야 함
        # 여기서는 간단히, 새로 생성된 경우에 대한 예시를 주석으로 남김
        # if driver and 'service' in locals():
        #     driver.quit()
        pass

if __name__ == '__main__':
    # 로컬 테스트를 위해 .env 파일 로드
    from dotenv import load_dotenv
    from pathlib import Path
    
    # .env_test 파일 경로 설정
    # 이 파일의 위치를 기준으로 프로젝트 루트를 찾고 .env_test를 찾음
    env_path = Path(__file__).resolve().parent.parent.parent / '.env_test'
    load_dotenv(dotenv_path=env_path)
    
    # Chrome을 디버깅 모드로 실행해야 Selenium이 연결할 수 있습니다.
    # 예: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    write_ekiss_mail()

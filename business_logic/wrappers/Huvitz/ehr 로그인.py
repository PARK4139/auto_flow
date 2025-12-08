import sys
from pathlib import Path
import traceback
import logging

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[3]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

# --- New Imports for EHR Login ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_pretty_html_string import get_pretty_html_string # Assuming this function exists


# Helper function to capture and log HTML for debugging
def _debug_html(driver, step_name):
    logging.debug(f"--- Debug HTML: {step_name} ---")
    try:
        html = driver.page_source
        pretty_html = get_pretty_html_string(html)
        logging.debug(f"Current HTML:\n{pretty_html}")
    except Exception as e:
        logging.error(f"Failed to capture HTML for debugging: {e}")

# Helper function to check if currently on the login page
def _check_if_on_login_page(driver):
    try:
        # Check for presence of login form elements or specific URL segment
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "S_USER_ID"))
        )
        logging.info("현재 로그인 페이지에 있습니다.")
        return True
    except:
        logging.warning("로그인 페이지가 아닌 것 같습니다.")
        return False

# Helper function to check if login is completed
def _check_if_login_completed(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "S_WORK_STA_BTN"))
        )
        if driver.find_element(By.ID, "S_WORK_STA_BTN").text == "업무시작":
            logging.info("로그인이 성공적으로 완료되었습니다. '업무시작' 버튼 확인.")
            return True
        else:
            logging.warning("로그인 완료 객체는 찾았으나 텍스트가 '업무시작'이 아닙니다.")
            return False
    except:
        logging.warning("로그인 완료 객체 ('S_WORK_STA_BTN')를 찾을 수 없습니다.")
        return False


if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    driver = None # Initialize driver to None
    try:
        ensure_window_title_replaced(get_nx(__file__))
        logging.info("EHR 로그인 스크립트 실행 시작.")

        # 1. Private Information Handling
        ehr_login_url = ensure_env_var_completed(key_name="EHR_LOGIN_URL", func_n=get_nx(__file__), guide_text="EHR 로그인 URL을 입력하세요:")
        ehr_user_id = ensure_env_var_completed(key_name="EHR_USER_ID", func_n=get_nx(__file__), guide_text="EHR 사용자 ID를 입력하세요:")
        ehr_password = ensure_env_var_completed(key_name="EHR_PASSWORD", func_n=get_nx(__file__), guide_text="EHR 비밀번호를 입력하세요:", mask_log=True)

        if not all([ehr_login_url, ehr_user_id, ehr_password]):
            logging.error("필수 로그인 정보가 부족합니다. 스크립트를 종료합니다.")
            sys.exit(1)

        # 2. Initialize WebDriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window() # Maximize window for better visibility

        logging.info(f"EHR 로그인 페이지로 이동: {ehr_login_url}")
        driver.get(ehr_login_url)

        _debug_html(driver, "초기 로그인 페이지")

        if not _check_if_on_login_page(driver):
            logging.error("현재 페이지가 로그인 페이지가 아닌 것 같습니다. URL을 확인하거나 수동으로 접근하십시오.")
            sys.exit(1)

        # 3. UI Interaction - Input ID and PW
        logging.info("ID와 비밀번호 입력 중...")
        user_id_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "S_USER_ID")))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "S_PWD")))

        user_id_field.send_keys(ehr_user_id)
        password_field.send_keys(ehr_password)

        _debug_html(driver, "ID/PW 입력 후")

        # 4. UI Interaction - Click Login Button
        logging.info("로그인 버튼 클릭 중...")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn_login")))
        login_button.click()

        # 5. Check Login Completion
        logging.info("로그인 완료 확인 중...")
        _debug_html(driver, "로그인 시도 후")

        if _check_if_login_completed(driver):
            logging.info("EHR 로그인 성공!")
            # Core logic after successful login (if any) can go here
            # Keep browser open for user to see, or close after a delay
            # time.sleep(5) # Example: keep open for 5 seconds
        else:
            logging.error("EHR 로그인 실패 또는 완료 객체를 찾을 수 없습니다. 수동 확인이 필요합니다.")
            _debug_html(driver, "로그인 실패 시")
            sys.exit(1)

    except Exception as exception:
        logging.error("EHR 로그인 스크립트 실행 중 예외 발생.", exc_info=True)
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        if 'driver' in locals() and driver: # Ensure driver is closed even on error
            logging.info("브라우저 종료 중...")
            driver.quit()
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
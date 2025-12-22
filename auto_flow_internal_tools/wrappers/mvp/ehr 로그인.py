import logging
import sys
import traceback

# --- New Imports for EHR Login ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_mouse_clicked_by_coordination_history import \
    ensure_mouse_clicked_by_coordination_history
from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import \
    ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import \
    ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_pretty_html_string import \
    get_pretty_html_string  # Assuming this function exists
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT


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
    except Exception as e:
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
    except Exception as e:
        logging.warning("로그인 완료 객체 ('S_WORK_STA_BTN')를 찾을 수 없습니다.")
        return False


if __name__ == "__main__":
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    driver = None  # Initialize driver to None
    try:
        ensure_window_title_replaced(get_nx(__file__))
        logging.info("EHR 로그인 스크립트 실행 시작.")

        # 1. Private Information Handling
        func_n = get_caller_name()
        ehr_login_url = ensure_env_var_completed(key_name="EHR_LOGIN_URL", func_n=func_n,
                                                 guide_text="EHR 로그인 URL을 입력하세요:")
        ehr_user_id = ensure_env_var_completed(key_name="EHR_USER_ID", func_n=func_n, guide_text="EHR 사용자 ID를 입력하세요:")
        ehr_password = ensure_env_var_completed(key_name="EHR_PASSWORD", func_n=func_n, guide_text="EHR 비밀번호를 입력하세요:",
                                                mask_log=True)

        if not all([ehr_login_url, ehr_user_id, ehr_password]):
            logging.error("필수 로그인 정보가 부족합니다. 스크립트를 종료합니다.")
            sys.exit(1)

        # 2. Initialize WebDriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()  # Maximize window for better visibility

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
            alert_as_gui("EHR 로그인 성공!")
            ensure_mouse_clicked_by_coordination_history(key_name="http 권한 허용", func_n=func_n)
            ensure_mouse_clicked_by_coordination_history(key_name="비밀번호 변경 확인", func_n=func_n)
            ensure_paused()
        else:
            logging.error("EHR 로그인 실패 또는 완료 객체를 찾을 수 없습니다. 수동 확인이 필요합니다.")
            _debug_html(driver, "로그인 실패 시")
            sys.exit(1)

    except Exception as e:
        logging.error("EHR 로그인 스크립트 실행 중 예외 발생.", exc_info=True)
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        if 'driver' in locals() and driver:  # Ensure driver is closed even on error
            logging.info("스크립트 완료. 브라우저를 열어둡니다.")
            # driver.quit()
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)

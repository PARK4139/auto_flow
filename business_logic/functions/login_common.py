import sys
from pathlib import Path
import traceback
import logging

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)


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


def common_login(
        driver: webdriver.Chrome,
        login_url: str,
        user_id: str,
        password: str,
        id_field_id: str,
        password_field_id: str,
        login_button_id: str,
        login_check_element_id: str,
        login_check_element_text: str,
        initial_check_element_id: str, # For checking if on login page initially
        func_n: str, # Caller function name for env var completion
        debug_html_func=None, # Function to call for debugging HTML
) -> bool:
    """
    Performs a common Selenium-based login process.

    Args:
        driver: Selenium WebDriver instance.
        login_url: The URL of the login page.
        user_id: The user ID for login.
        password: The password for login.
        id_field_id: The HTML ID of the user ID input field.
        password_field_id: The HTML ID of the password input field.
        login_button_id: The HTML ID of the login button.
        login_check_element_id: The HTML ID of the element to check for successful login.
        login_check_element_text: The expected text content of the login check element.
        initial_check_element_id: The HTML ID of an element present on the initial login page to confirm.
        func_n: The name of the calling function for environment variable completion.
        debug_html_func: Optional function to call for debugging HTML at critical steps.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    if debug_html_func is None:
        debug_html_func = _debug_html # Use internal _debug_html if not provided

    logging.info(f"로그인 페이지로 이동: {login_url}")
    driver.get(login_url)

    debug_html_func(driver, "초기 로그인 페이지")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, initial_check_element_id))
        )
        logging.info("현재 로그인 페이지에 있습니다.")
    except:
        logging.error("현재 페이지가 예상 로그인 페이지가 아닌 것 같습니다. URL을 확인하십시오.")
        return False

    logging.info("ID와 비밀번호 입력 중...")
    user_id_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_field_id)))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, password_field_id)))

    user_id_field.send_keys(user_id)
    password_field.send_keys(password)

    debug_html_func(driver, "ID/PW 입력 후")

    logging.info("로그인 버튼 클릭 중...")
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, login_button_id)))
    login_button.click()

    logging.info("로그인 완료 확인 중...")
    debug_html_func(driver, "로그인 시도 후")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, login_check_element_id))
        )
        if login_check_element_text: # Only check text if it's provided
            actual_text = driver.find_element(By.ID, login_check_element_id).text
            if actual_text == login_check_element_text:
                logging.info(f"로그인이 성공적으로 완료되었습니다. '{login_check_element_text}' 객체 확인.")
                return True
            else:
                logging.warning(f"로그인 완료 객체는 찾았으나 텍스트가 '{login_check_element_text}'이 아닙니다. 실제 텍스트: '{actual_text}'")
                return False
        else: # If no specific text is provided, just check for element presence
            logging.info(f"로그인이 성공적으로 완료되었습니다. '{login_check_element_id}' 객체 확인 (텍스트 검증 제외).")
            return True
    except:
        logging.error(f"로그인 완료 객체 ('{login_check_element_id}')를 찾을 수 없습니다.")
        debug_html_func(driver, "로그인 실패 시")
        return False

# Example usage (not part of the common function, but for testing or direct execution)
if __name__ == "__main__":
    # This block would be in your wrapper script, not in login_common.py
    # This is just for demonstration of how common_login would be called.
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    driver = None
    try:
        ensure_window_title_replaced(get_nx(__file__))
        logging.info("common_login 함수 테스트 시작.")

        test_login_url = ensure_env_var_completed(key_name="TEST_LOGIN_URL", func_n=get_nx(__file__), guide_text="테스트 로그인 URL을 입력하세요:")
        test_user_id = ensure_env_var_completed(key_name="TEST_USER_ID", func_n=get_nx(__file__), guide_text="테스트 사용자 ID를 입력하세요:")
        test_password = ensure_env_var_completed(key_name="TEST_PASSWORD", func_n=get_nx(__file__), guide_text="테스트 비밀번호를 입력하세요:", mask_log=True)

        if not all([test_login_url, test_user_id, test_password]):
            logging.error("필수 테스트 로그인 정보가 부족합니다. 스크립트를 종료합니다.")
            sys.exit(1)

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()

        login_successful = common_login(
            driver=driver,
            login_url=test_login_url,
            user_id=test_user_id,
            password=test_password,
            id_field_id="txtId", # Example for common fields
            password_field_id="txtPwd", # Example for common fields
            login_button_id="btnLogin", # Example for common fields
            login_check_element_id="Left_Navigator_lblMail", # Example for common fields
            login_check_element_text="", # Check only for presence, not specific text
            initial_check_element_id="txtId", # Example: check for ID field on login page
            func_n=get_nx(__file__),
            debug_html_func=_debug_html,
        )

        if login_successful:
            logging.info("common_login 테스트 성공!")
        else:
            logging.error("common_login 테스트 실패.")

    except Exception as exception:
        logging.error("common_login 테스트 중 예외 발생.", exc_info=True)
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        if driver:
            input("continue:enter") # Pause before quitting the browser
            logging.info("브라우저 종료 중...")
            driver.quit()
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

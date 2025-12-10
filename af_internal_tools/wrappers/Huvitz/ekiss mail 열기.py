import logging
import sys
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
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

# --- New Imports for Mail Login ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_pretty_html_string import \
    get_pretty_html_string  # Assuming this function exists
from af_internal_tools.functions.login_common import common_login
from af_internal_tools.functions.close_popups import close_known_popups


# Helper function to capture and log HTML for debugging
def _debug_html(driver, step_name):
    logging.debug(f"--- Debug HTML: {step_name} ---")
    try:
        html = driver.page_source
        pretty_html = get_pretty_html_string(html)
        logging.debug(f"Current HTML:\n{pretty_html}")
    except Exception as e:
        logging.error(f"Failed to capture HTML for debugging: {e}")


# Helper function to check if currently on the mail login page
def _check_if_on_mail_login_page(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtId"))
        )
        logging.info("현재 메일 로그인 페이지에 있습니다.")
        return True
    except:
        logging.warning("메일 로그인 페이지가 아닌 것 같습니다.")
        return False


# Helper function to check if on the mail main page (after successful login)
def _check_if_on_main_page(driver, expected_main_url):
    current_url = driver.current_url
    if current_url.startswith(expected_main_url):  # Use startswith for partial URL match
        logging.info(f"메인 페이지에 성공적으로 진입했습니다. 현재 URL: {current_url}")
        return True
    else:
        logging.warning(f"메인 페이지 진입 실패. 현재 URL: {current_url}, 예상 URL: {expected_main_url}")
        return False


# Helper function to check if on the mail window (after clicking mail button)
def _check_if_on_mail_window(driver, expected_mail_window_url):
    current_url = driver.current_url
    if current_url.startswith(expected_mail_window_url):  # Use startswith for partial URL match
        logging.info(f"메일 창에 성공적으로 진입했습니다. 현재 URL: {current_url}")
        return True
    else:
        logging.warning(f"메일 창 진입 실패. 현재 URL: {current_url}, 예상 URL: {expected_mail_window_url}")
        return False


if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    driver = None  # Initialize driver to None
    try:
        func_n = get_caller_name()
        ensure_window_title_replaced(get_nx(__file__))
        logging.info("Huvitz Mail 열기 스크립트 실행 시작.")

        # 1. Private Information Handling - using EKISS variables as per user feedback
        ekiss_login_url = ensure_env_var_completed(key_name="EKISS_LOGIN_URL", func_n=func_n,
                                                   guide_text="EKISS 로그인 URL을 입력하세요:")
        ekiss_user_id = ensure_env_var_completed(key_name="EKISS_USER_ID", func_n=func_n,
                                                 guide_text="EKISS 사용자 ID를 입력하세요:")
        ekiss_password = ensure_env_var_completed(key_name="EKISS_PASSWORD", func_n=func_n,
                                                  guide_text="EKISS 비밀번호를 입력하세요:", mask_log=True)
        mail_main_url = ensure_env_var_completed(key_name="MAIL_MAIN_URL", func_n=func_n,
                                                 guide_text="로그인 후 메인 페이지 URL을 입력하세요:")
        mail_window_url = ensure_env_var_completed(key_name="MAIL_WINDOW_URL", func_n=func_n,
                                                   guide_text="메일 창 URL을 입력하세요:")

        if not all([ekiss_login_url, ekiss_user_id, ekiss_password, mail_main_url, mail_window_url]):
            logging.error("필수 메일 또는 EKISS 로그인 정보가 부족합니다. 스크립트를 종료합니다.")
            sys.exit(1)

        # 2. Initialize WebDriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()  # Maximize window for better visibility

        # 3. Perform common login to EKISS
        login_successful = common_login(
            driver=driver,
            login_url=ekiss_login_url,
            user_id=ekiss_user_id,
            password=ekiss_password,
            id_field_id="txtId",
            password_field_id="txtPwd",
            login_button_id="btnLogin",
            login_check_element_id="Left_Navigator_lblMail",  # Or another suitable element for EKISS main page
            login_check_element_text="",  # Only check for presence
            initial_check_element_id="txtId",
            func_n=func_n,
            debug_html_func=_debug_html,
        )

        if not login_successful:
            logging.error("EKISS 로그인 실패. 메일 열기 스크립트를 종료합니다.")
            sys.exit(1)

        logging.info("EKISS 로그인 성공. 팝업 닫기 시도 중.")
        _debug_html(driver, "로그인 성공 직후 - 팝업 닫기 전")  # Add this line
        close_known_popups(driver)  # Close any pop-ups after login

        # 4. Check Login Completion (Main Page - after popups)
        # Assuming after popups, we are still on the main page. Re-check URL if necessary.
        logging.info("메인 페이지 진입 확인 중 (팝업 닫은 후)...")
        WebDriverWait(driver, 30).until(EC.url_to_be(mail_main_url))  # Wait until URL matches main page
        _debug_html(driver, "팝업 닫은 후 메인 페이지")

        if not _check_if_on_main_page(driver, mail_main_url):
            logging.error("메일 메인 페이지 진입 실패 (팝업 닫은 후). 수동 확인이 필요합니다.")
            sys.exit(1)

        # 5. Click Mail Button
        logging.info("메일 버튼 클릭 시도 중...")
        _debug_html(driver, "메일 버튼 클릭 시도 전") # Debug before click attempt
        try:
            mail_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//a[contains(@onclick, 'go_email()') and .//img[contains(@src, '/Images/common/icon_mail.png')]]"))
            )
            mail_button.click()
            logging.info("메일 버튼 클릭 성공.")
        except Exception as e:
            logging.error(f"메일 버튼 클릭 실패: {e}", exc_info=True)
            _debug_html(driver, "메일 버튼 클릭 실패 후") # Debug after click failure
            logging.error(f"현재 URL: {driver.current_url}")
            sys.exit(1)

        # 6. Check Mail Window
        logging.info("메일 창 진입 확인 중...")
        try:
            WebDriverWait(driver, 30).until(EC.url_to_be(mail_window_url))  # Wait until URL matches mail window
            _debug_html(driver, "메일 창 진입 후")

            if _check_if_on_mail_window(driver, mail_window_url):
                logging.info("메일 창 열기 성공!")
            else:
                logging.error(f"메일 창 진입 실패. 현재 URL: {driver.current_url}. 예상 URL: {mail_window_url}. 수동 확인이 필요합니다.")
                _debug_html(driver, "메일 창 진입 실패 후")
                sys.exit(1)
        except Exception as e:
            logging.error(f"메일 창 진입 대기 중 타임아웃 또는 기타 오류 발생: {e}", exc_info=True)
            _debug_html(driver, "메일 창 진입 대기 중 오류 발생 후")
            logging.error(f"현재 URL: {driver.current_url}")
            sys.exit(1)



    except Exception as exception:
        logging.error("Huvitz Mail 열기 스크립트 실행 중 예외 발생.", exc_info=True)
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        if driver:
            input("팝업 닫기 시도 완료. 브라우저를 확인하시고 엔터를 누르면 종료됩니다.")
            logging.info("브라우저 종료 중...")
            driver.quit()
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

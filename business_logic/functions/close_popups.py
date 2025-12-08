import sys
from pathlib import Path
import logging
import time

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    logging.error("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# PK Internal Tools imports (moved to top for module-level availability)
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

# Specific import for common_login (since it's a peer module)
from business_logic.functions.login_common import common_login

from pk_internal_tools.pk_functions.get_pretty_html_string import get_pretty_html_string

# Helper function to capture and log HTML for debugging
def _debug_html(driver, step_name):
    logging.debug(f"--- Debug HTML: {step_name} ---")
    try:
        html = driver.page_source
        pretty_html = get_pretty_html_string(html)
        logging.debug(f"Current HTML:\n{pretty_html}")
    except Exception as e:
        logging.error(f"Failed to capture HTML for debugging: {e}")

def close_known_popups(driver: webdriver.Chrome):
    """
    Attempts to close known pop-up windows that may appear after login.

    Args:
        driver: The Selenium WebDriver instance.
    """
    logging.info("로그인 후 알려진 팝업 닫기 시도 중...")

    # --- Pop-up 2: div with id "divpop" (Process first due to potential blocking) ---
    logging.info("팝업 2 (divpop) 감지 시도 중...")
    try:
        # Check for the presence of the divpop element
        divpop_element = WebDriverWait(driver, 5).until( # Increased wait time
            EC.presence_of_element_located((By.ID, "divpop"))
        )
        if divpop_element.is_displayed():
            logging.info("팝업 2 (divpop) 발견. 닫기 버튼 클릭 시도 중...")
            close_button = WebDriverWait(driver, 5).until( # Increased wait time
                EC.element_to_be_clickable((By.XPATH, "//div[@id='divpop']//a[contains(@onclick, 'closeWin()')]"))
            )
            close_button.click()
            logging.info("팝업 2 닫기 성공.")
            _debug_html(driver, "팝업 2 닫은 후")
            time.sleep(1) # Wait for page to stabilize after closing
        else:
             logging.info("팝업 2 (divpop)은 현재 페이지에 있지만 표시되지 않습니다. 건너뜁니다.")
    except TimeoutException:
        logging.info("팝업 2 (divpop) 요소를 찾지 못했습니다 (Timeout). 팝업이 없을 수 있습니다.")
    except NoSuchElementException:
        logging.info("팝업 2 (divpop) 요소를 찾지 못했습니다 (NoSuchElement). 팝업이 없을 수 있습니다.")
    except Exception as e:
        logging.warning(f"팝업 2 처리 중 예상치 못한 예외 발생: {e}", exc_info=True)

    # --- Pop-up 1: div with class "popup-box" and a specific h2 title ---
    logging.info("팝업 1 (마감일정 안내) 감지 시도 중...")
    try:
        # Check for the presence of the popup-box div and its title
        popup_box_element = WebDriverWait(driver, 5).until( # Increased wait time
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.popup-box h2"))
        )
        if "마감일정 안내" in popup_box_element.text: # More robust check for the specific popup
            logging.info("팝업 1 (마감일정 안내) 발견. 닫기 버튼 클릭 시도 중...")
            close_button = WebDriverWait(driver, 5).until( # Increased wait time
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.popup-box a.popup-close"))
            )
            close_button.click()
            logging.info("팝업 1 닫기 성공.")
            _debug_html(driver, "팝업 1 닫은 후")
            time.sleep(1) # Wait for page to stabilize after closing
        else:
            logging.info("팝업 1 (마감일정 안내)는 현재 페이지에 있지만 내용이 다릅니다. 건너뜁니다.")
    except TimeoutException:
        logging.info("팝업 1 (마감일정 안내) 요소를 찾지 못했습니다 (Timeout). 팝업이 없을 수 있습니다.")
    except NoSuchElementException:
        logging.info("팝업 1 (마감일정 안내) 요소를 찾지 못했습니다 (NoSuchElement). 팝업이 없을 수 있습니다.")
    except Exception as e:
        logging.warning(f"팝업 1 처리 중 예상치 못한 예외 발생: {e}", exc_info=True)

    logging.info("알려진 팝업 닫기 시도 완료.")

    # Example usage (for testing this module directly)

    if __name__ == "__main__":

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

        driver = None

        try:
            ensure_window_title_replaced(get_nx(__file__))
            logging.info("close_known_popups 함수 테스트 시작. (EKISS 로그인 시도 후 팝업 닫기)")

            # For testing, we need to log into EKISS first
            # Re-using common_login function's test variables for simplicity
            ekiss_login_url = ensure_env_var_completed(key_name="TEST_LOGIN_URL", func_n=get_nx(__file__), guide_text="EKISS 로그인 URL을 입력하세요:")
            ekiss_user_id = ensure_env_var_completed(key_name="TEST_USER_ID", func_n=get_nx(__file__), guide_text="EKISS 사용자 ID를 입력하세요:")
            ekiss_password = ensure_env_var_completed(key_name="TEST_PASSWORD", func_n=get_nx(__file__), guide_text="EKISS 비밀번호를 입력하세요:", mask_log=True)

            if not all([ekiss_login_url, ekiss_user_id, ekiss_password]):
                logging.error("EKISS 로그인 정보가 부족합니다. 스크립트를 종료합니다.")
                sys.exit(1)

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            driver.maximize_window()

            # Temporarily perform login to reach a state where popups might appear
            
            login_successful = common_login(
                driver=driver,
                login_url=ekiss_login_url,
                user_id=ekiss_user_id,
                password=ekiss_password,
                id_field_id="txtId",
                password_field_id="txtPwd",
                login_button_id="btnLogin",
                login_check_element_id="Left_Navigator_lblMail",
                login_check_element_text="", # Only check for presence
                initial_check_element_id="txtId",
                func_n=get_nx(__file__),
                debug_html_func=_debug_html,
            )

            if login_successful:
                logging.info("EKISS 로그인 성공. 팝업 닫기 함수 호출 시도.")
                close_known_popups(driver)
                input("팝업 닫기 시도 완료. 브라우저를 확인하시고 엔터를 누르면 종료됩니다.")
            else:
                logging.error("EKISS 로그인 실패. 팝업 닫기 테스트를 진행할 수 없습니다.")
                _debug_html(driver, "로그인 실패 후 팝업 닫기 시도 전")

        except Exception as exception:
            logging.error("close_known_popups 테스트 중 예외 발생.", exc_info=True)
            ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
        finally:
            if driver:
                logging.info("브라우저 종료 중...")
                driver.quit()
            ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)

import pytest
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Ensure the project root is in the path to allow imports from af_internal_tools, etc.
# This is a common pattern for tests.
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from af_internal_tools.functions.login_common import common_login
from af_internal_tools.functions.close_popups import close_known_popups

from pk_internal_tools.pk_objects.pk_tester import PkTester

# Load test environment variables from .env_test
PkTester.load_test_env()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def driver():
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.
    This runs once per module.
    """
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    logger.info("Closing WebDriver.")
    driver.quit()

def test_ekiss_login_and_mail_button_interaction(driver):
    """
    Tests the full EKISS login flow. It verifies that after logging in and attempting
    to close popups, the main page is interactive by clicking the 'Mail' link.
    
    This test is designed to fail if a popup (like 'divpop') is not closed correctly
    and intercepts the click on the mail link.
    """
    logger.info("Starting EKISS login and mail button interaction test.")
    
    # 1. Get credentials from environment variables (loaded by PkTester.load_test_env())
    ekiss_login_url = os.environ.get("TEST_LOGIN_URL")
    ekiss_user_id = os.environ.get("TEST_USER_ID")
    ekiss_password = os.environ.get("TEST_PASSWORD")
    
    # Assert that environment variables are indeed loaded
    assert all([ekiss_login_url, ekiss_user_id, ekiss_password]), "Required test environment variables are not set. Ensure .env_test is configured correctly."
    
    # 2. Perform login using the common login function
    logger.info(f"Attempting to log into {ekiss_login_url}")
    login_successful = common_login(
        driver=driver,
        login_url=ekiss_login_url,
        user_id=ekiss_user_id,
        password=ekiss_password,
        id_field_id="txtId",
        password_field_id="txtPwd",
        login_button_id="btnLogin",
        login_check_element_id="Left_Navigator_lblMail",
        login_check_element_text="",  # Check for presence only
        initial_check_element_id="txtId",
        func_n="test_ekiss_login_and_mail_button_interaction", # Pass function name for logging context
        debug_html_func=None # Use default debugger
    )
    
    assert login_successful, "EKISS login failed. Check credentials and login page elements."
    logger.info("Login successful.")

    # 3. Attempt to close known popups (this is the function under test)
    logger.info("Calling close_known_popups().")
    close_known_popups(driver)
    logger.info("Finished close_known_popups().")

    # 4. Verify main page is interactive by clicking the "Mail" link
    # This is the assertion step. It should fail if a popup is blocking the UI.
    try:
        logger.info("Attempting to find and click the 'Mail' link (Left_Navigator_lblMail).")
        mail_link = driver.find_element(By.ID, "Left_Navigator_lblMail")
        mail_link.click()
        logger.info("Successfully clicked the 'Mail' link. The page seems to be interactive.")
        # If the click succeeds, the test passes.
    except ElementClickInterceptedException as e:
        pytest.fail(
            "FAIL: The 'Mail' link click was intercepted, likely by an unclosed popup. "
            f"This confirms the bug in close_known_popups. Details: {e}"
        )
    except Exception as e:
        pytest.fail(
            "An unexpected error occurred while trying to click the 'Mail' link. "
            f"Error: {e}"
        )

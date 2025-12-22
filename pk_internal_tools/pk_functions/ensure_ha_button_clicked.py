import logging
from typing import Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pk_internal_tools.pk_functions.ensure_env_var_completed import (
    ensure_env_var_completed,
)
from pk_internal_tools.pk_functions.ensure_ha_onboarding_locator_resolved import (
    ensure_ha_onboarding_locator_resolved,
)


def ensure_ha_button_clicked(
    driver,
    wait: WebDriverWait,
    *,
    ha_url: str,
    default_text: Optional[str],
    button_text_env_key: str,
    locator_env_key: str,
    description: str,
    timeout_seconds: Optional[int] = None,
) -> bool:
    """
    Home Assistant 온보딩 화면에서 특정 텍스트를 가진 버튼을 찾아 클릭합니다.
    버튼 텍스트는 사용자에게 입력받고, 기본 텍스트는 초기 값으로만 사용합니다.
    기본 텍스트로 찾기를 시도하고 실패하면 환경 변수 기반 locator 요청으로 대체합니다.
    """
    timeout = timeout_seconds or wait._timeout  # noqa: SLF001

    button_text = default_text
    if button_text_env_key:
        user_button_text = ensure_env_var_completed(
            key_name=button_text_env_key,
            func_n="ensure_ha_button_clicked",
            guide_text=(
                f"{description} 버튼의 표시 텍스트를 입력하세요."
                f"{f' (기본값: {default_text})' if default_text else ''}"
            ),
        )
        if user_button_text:
            button_text = user_button_text.strip()

    if not button_text:
        logging.warning("%s 버튼 텍스트가 비어 있습니다. locator 입력을 요청합니다.", description)

    def _try_locator(locator):
        try:
            button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button.click()
            logging.info("%s 클릭 성공: %s", description, locator)
            return True
        except TimeoutException:
            logging.debug("%s locator 클릭 실패(Timeout): %s", description, locator)
            return False
        except Exception as exc:
            logging.debug("%s locator 클릭 실패: %s", description, exc)
            return False

    # 1) HTTP 요청 기반으로 locator 추론
    auto_locator = ensure_ha_onboarding_locator_resolved(
        ha_url=ha_url,
        button_text=button_text,
    )
    if auto_locator and _try_locator(auto_locator):
        return True

    # 2) Shadow DOM / 커스텀 요소를 포함한 텍스트 기반 검색
    if button_text and _click_button_via_text_search(driver, button_text, description):
        return True

    # 3) 사용자 정의 텍스트로 시도 (Selenium DOM 기준)
    if button_text:
        locator = (By.XPATH, f"//button[contains(normalize-space(.), '{button_text}')]")
        if _try_locator(locator):
            return True

    # 4) 사용자가 지정한 locator 요청
    locator_str = ensure_env_var_completed(
        key_name=locator_env_key,
        func_n="ensure_ha_button_clicked",
        guide_text=(
            f"{description} 버튼을 찾기 위한 locator를 입력하세요.\n"
            "형식 예시:\n"
            "  css:button[data-test='start']\n"
            "  xpath://button[contains(., '시작')]\n"
            "  text:나만의 스마트 홈 만들기\n"
        ),
    )
    locator = _locator_from_string(locator_str)
    if not locator:
        logging.error("%s locator 정보를 가져오지 못했습니다.", description)
        return False

    return _try_locator(locator)


def _click_button_via_text_search(driver, button_text: str, description: str) -> bool:
    if not button_text:
        return False

    script = """
        const targetText = arguments[0]?.trim().toLowerCase();
        if (!targetText) { return false; }

        const CANDIDATE_SELECTORS = [
            'button',
            'ha-button',
            'mwc-button',
            'ha-card button',
            'ha-card ha-button',
            'ha-card mwc-button',
            'ha-call-to-action-button',
        ];

        function normalize(text) {
            if (!text) return '';
            return text.replace(/\\s+/g, ' ').trim().toLowerCase();
        }

        function matchesText(element) {
            if (!element) return false;
            const textContent = element.textContent || element.innerText;
            if (!textContent) return false;
            return normalize(textContent).includes(targetText);
        }

        function search(root, depth = 0) {
            if (!root || depth > 8) return null;

            if (root.querySelectorAll) {
                for (const selector of CANDIDATE_SELECTORS) {
                    const nodes = root.querySelectorAll(selector);
                    for (const node of nodes) {
                        if (matchesText(node)) {
                            return node;
                        }
                    }
                }
            }

            const children = root.children || [];
            for (const child of children) {
                const found = search(child, depth + 1);
                if (found) return found;
            }

            if (root.shadowRoot) {
                const found = search(root.shadowRoot, depth + 1);
                if (found) return found;
            }

            return null;
        }

        const foundNode = search(document.body);
        if (!foundNode) return false;

        foundNode.scrollIntoView({behavior: 'smooth', block: 'center'});
        try {
            foundNode.click();
            return true;
        } catch (err) {
            console.error('Shadow DOM click failed', err);
            return false;
        }
    """

    try:
        clicked = driver.execute_script(script, button_text)
        if clicked:
            logging.info("%s 텍스트 기반 shadow DOM 검색으로 클릭 성공", description)
        return bool(clicked)
    except Exception as exc:
        logging.debug("%s 텍스트 기반 shadow DOM 검색 실패: %s", description, exc)
        return False


def _locator_from_string(value: str):
    if not value:
        return None
    lower = value.lower()
    if lower.startswith("css:"):
        return By.CSS_SELECTOR, value[4:].strip()
    if lower.startswith("xpath:"):
        return By.XPATH, value[6:].strip()
    if lower.startswith("text:"):
        text = value[5:].strip()
        return By.XPATH, f"//button[contains(normalize-space(.), '{text}')]"
    return By.CSS_SELECTOR, value.strip()


import logging
from typing import Optional, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def ensure_ha_onboarding_locator_resolved(
    ha_url: str,
    button_text: Optional[str],
    timeout_seconds: int = 5,
) -> Optional[Tuple[By, str]]:
    """
    Home Assistant 온보딩 페이지 HTML을 요청하여 버튼 텍스트 기반 locator를 추론합니다.
    구조가 바뀌더라도 텍스트/속성을 활용하여 최대한 안정적으로 locator를 생성합니다.
    """
    if not ha_url:
        logging.debug("[ensure_ha_locator] ha_url 이 비어 있어 locator를 추론할 수 없습니다.")
        return None

    onboarding_url = urljoin(ha_url.rstrip("/") + "/", "onboarding.html")
    logging.debug("[ensure_ha_locator] 온보딩 HTML 요청: %s", onboarding_url)

    try:
        resp = requests.get(onboarding_url, timeout=timeout_seconds)
        resp.raise_for_status()
    except Exception as exc:
        logging.warning("[ensure_ha_locator] 온보딩 HTML 요청 실패: %s", exc)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    normalized_target = _normalize_text(button_text)

    button_candidates = soup.find_all("button")
    if not button_candidates:
        logging.debug("[ensure_ha_locator] 버튼 요소가 감지되지 않았습니다.")
        return None

    # 1) 텍스트가 일치하거나 포함되는 버튼 우선 탐색
    if normalized_target:
        for button in button_candidates:
            btn_text = _normalize_text(button.get_text())
            if not btn_text:
                continue
            if normalized_target in btn_text or btn_text in normalized_target:
                locator = _build_locator_from_button(button, fallback_text=button_text)
                if locator:
                    logging.info(
                        "[ensure_ha_locator] 텍스트 기반 locator 추론 성공: %s", locator
                    )
                    return locator

    # 2) 텍스트 매칭에 실패하면 data-* / id / class 를 활용해 첫 번째 버튼 locator 생성
    for button in button_candidates:
        locator = _build_locator_from_button(button, fallback_text=button_text)
        if locator:
            logging.info(
                "[ensure_ha_locator] 텍스트 매칭 실패, 구조 기반 locator 사용: %s",
                locator,
            )
            return locator

    logging.debug("[ensure_ha_locator] 적절한 locator 를 생성하지 못했습니다.")
    return None


def _normalize_text(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    normalized = " ".join(value.split())
    return normalized.strip().lower()


def _build_locator_from_button(button, fallback_text: Optional[str]) -> Optional[Tuple[By, str]]:
    if not button:
        return None

    element_id = button.get("id")
    if element_id:
        return By.CSS_SELECTOR, f"button#{element_id}"

    data_test = button.get("data-test") or button.get("data-testid")
    if data_test:
        return By.CSS_SELECTOR, f"button[data-test='{data_test}']"

    class_list = button.get("class")
    if class_list:
        class_selector = ".".join(cls for cls in class_list if cls)
        if class_selector:
            return By.CSS_SELECTOR, f"button.{class_selector}"

    # fallback: XPath by text
    button_text = button.get_text(strip=True) or fallback_text
    if button_text:
        normalized_text = " ".join(button_text.split())
        return (
            By.XPATH,
            f"//button[contains(normalize-space(.), '{normalized_text}')]",
        )

    return None


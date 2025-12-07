import logging
import os
import time
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
    ensure_env_var_completed_2025_11_24,
)
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ha_selenium_driver_manager import (
    get_ha_selenium_driver,
)
from pk_internal_tools.pk_functions.ensure_ha_button_clicked import ensure_ha_button_clicked
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_home_assistant_onboarding_completed(
    ha_url: str,
    *,
    headless_mode: bool = False,
    timeout_seconds: int = 90,
) -> bool:
    """Automate HA onboarding: login-first check, then onboarding (fields, address, next)."""
    """
    Selenium을 활용하여 Home Assistant 초기 온보딩을 자동화합니다.
    1) "나만의 스마트 홈 만들기" 버튼 클릭
    2) 이름/사용자 이름/비밀번호/비밀번호 확인 입력
    3) "계정 만들기" 버튼 클릭
    이미 온보딩이 완료된 경우 True를 반환하고 즉시 종료합니다.
    """

    driver = None
    try:
        driver = get_ha_selenium_driver(headless_mode=headless_mode)
        wait = WebDriverWait(driver, timeout_seconds)

        # 온보딩 페이지로 직접 접근 시도
        onboarding_url = ha_url.rstrip("/") + "/onboarding.html"
        logging.info("Home Assistant 온보딩 자동화를 시작합니다. URL=%s", onboarding_url)
        driver.set_page_load_timeout(timeout_seconds)
        try:
            driver.get(onboarding_url)
        except Exception as e:
            logging.warning("온보딩 페이지 접근 실패, 루트 URL로 재시도: %s", e)
            onboarding_url = ha_url.rstrip("/") + "/"
            driver.get(onboarding_url)
        ensure_slept(milliseconds=2000)  # 페이지 로딩 대기 시간 증가
        # 접속 전/직후 진단: 페이지 메타 정보 로깅
        try:
            _log_pre_connection_diagnostics(driver, onboarding_url)
        except Exception as diag_exc:
            logging.debug("사전 접속 진단 중 경미한 오류: %s", diag_exc)

        initial_html = driver.page_source

        # 로그인 페이지 여부를 최우선으로 점검
        try:
            # 로그인에 필요한 최소 자격 정보를 먼저 확보 (이미 .env에 있으면 즉시 사용)
            ha_user_name_for_login = ensure_env_var_completed_2025_11_24(
                key_name="ha_onboarding_username",
                func_n="ensure_home_assistant_onboarding_completed",
                guide_text="Home Assistant 계정 사용자 이름을 입력하세요:",
            )
            ha_password_for_login = ensure_env_var_completed_2025_11_24(
                key_name="ha_onboarding_password",
                func_n="ensure_home_assistant_onboarding_completed",
                guide_text="Home Assistant 계정 비밀번호를 입력하세요:",
            )
            # 로그인 페이지인지 판별하고, 맞다면 즉시 로그인 시도
            shallow_u, deep_u = _get_selector_counts(driver, "input[name='username'], input.mdc-text-field__input[name='username']")
            shallow_p, deep_p = _get_selector_counts(driver, "input[name='password'], input.mdc-text-field__input[name='password']")
            is_login_detected = ("집에 오신 것을 환영합니다" in initial_html) or (deep_u > 0 and deep_p > 0)
            logging.info("로그인 선검사: is_login_detected=%s shallow_u=%s deep_u=%s shallow_p=%s deep_p=%s",
                         is_login_detected, shallow_u, deep_u, shallow_p, deep_p)
            if is_login_detected:
                logging.info("로그인 페이지가 먼저 감지되었습니다. 로그인 절차를 진행합니다.")
                if _handle_login_step(
                    driver=driver,
                    wait=wait,
                    user_name=ha_user_name_for_login,
                    password=ha_password_for_login,
                    ha_url=ha_url,
                ):
                    logging.info("로그인 자동화가 완료되었습니다.")
                    # 로그인 직후 페이지 판별 후 위치(주소) 단계가 나타나면 처리
                    page_after_login = _detect_current_page(driver)
                    logging.info("로그인 직후 페이지 판별 결과: %s", page_after_login)
                    if page_after_login == "onboarding_location":
                        address_query_after_login = ensure_env_var_completed_2025_11_24(
                            key_name="ha_onboarding_address_search_text",
                            func_n="ensure_home_assistant_onboarding_completed",
                            guide_text="Home Assistant 주소 검색에 사용할 값을 입력하세요 (예: 관평로 333):",
                        )
                        if not _handle_location_step(driver, wait, address_query_after_login, ha_url):
                            logging.warning("로그인 이후 주소 입력 단계 자동화가 완료되지 않았습니다.")
                            return False
                        logging.info("로그인 이후 위치 단계까지 완료되었습니다.")
                    elif page_after_login == "onboarding_country":
                        if not _handle_country_step(driver, wait, ha_url):
                            logging.warning("로그인 이후 국가 설정 단계 자동화가 완료되지 않았습니다.")
                            return False
                        logging.info("로그인 이후 국가 설정 단계까지 완료되었습니다.")
                    elif page_after_login == "onboarding_help":
                        if not _handle_help_us_page(driver, wait, ha_url):
                            logging.warning("로그인 이후 도움 페이지 단계 자동화가 완료되지 않았습니다.")
                            return False
                        logging.info("로그인 이후 도움 페이지 단계까지 완료되었습니다.")
                    elif page_after_login == "onboarding_ready":
                        if not _handle_ready_page(driver, wait, ha_url):
                            logging.warning("로그인 이후 준비 완료 페이지 단계 자동화가 완료되지 않았습니다.")
                            return False
                        logging.info("로그인 이후 준비 완료 페이지 단계까지 완료되었습니다.")
                    return True
                logging.warning("로그인 자동화에 실패했습니다.")
                return False
        except Exception as _e:
            logging.debug("로그인 선검사 중 경미한 오류: %s", _e)

        # 온보딩 필요 여부 확인 (더 관대하게 체크)
        needs_onboarding = _needs_onboarding(initial_html)
        current_url = driver.current_url
        is_onboarding_page = "/onboarding" in current_url or "onboarding" in current_url.lower()
        
        if not needs_onboarding and not is_onboarding_page:
            logging.info("온보딩 화면이 감지되지 않았습니다. 이미 완료된 것으로 판단합니다.")
            return True

        # 버튼 클릭 시도 (온보딩 페이지인 경우 무조건 시도)
        logging.info("온보딩 시작 버튼 클릭을 시도합니다.")
        button_clicked = ensure_ha_button_clicked(
            driver=driver,
            wait=wait,
            ha_url=ha_url,
            default_text="나만의 스마트 홈 만들기",
            button_text_env_key="ha_onboarding_start_button_text",
            locator_env_key="ha_onboarding_start_button_locator",
            description="온보딩 시작 버튼",
        )
        
        if not button_clicked:
            logging.warning("온보딩 시작 버튼을 클릭하지 못했습니다. 페이지 상태를 확인하세요.")
            ensure_slept(milliseconds=1000)  # 페이지 변화 대기

        # 입력값 확보
        ha_full_name = ensure_env_var_completed_2025_11_24(
            key_name="ha_onboarding_full_name",
            func_n="ensure_home_assistant_onboarding_completed",
            guide_text="Home Assistant 계정에 사용할 이름을 입력하세요:",
        )
        ha_user_name = ensure_env_var_completed_2025_11_24(
            key_name="ha_onboarding_username",
            func_n="ensure_home_assistant_onboarding_completed",
            guide_text="Home Assistant 계정 사용자 이름을 입력하세요:",
        )
        ha_password = ensure_env_var_completed_2025_11_24(
            key_name="ha_onboarding_password",
            func_n="ensure_home_assistant_onboarding_completed",
            guide_text="Home Assistant 계정 비밀번호를 입력하세요:",
        )
        ha_password_confirm = ensure_env_var_completed_2025_11_24(
            key_name="ha_onboarding_password_confirm",
            func_n="ensure_home_assistant_onboarding_completed",
            guide_text="비밀번호 확인을 위해 다시 입력하세요:",
        )

        _fill_onboarding_form(
            driver=driver,
            wait=wait,
            full_name=ha_full_name,
            user_name=ha_user_name,
            password=ha_password,
            password_confirm=ha_password_confirm,
        )

        logging.info("계정 만들기 버튼 클릭을 시도합니다.")
        create_clicked = ensure_ha_button_clicked(
            driver=driver,
            wait=wait,
            ha_url=ha_url,
            default_text="계정 만들기",
            button_text_env_key="ha_onboarding_create_button_text",
            locator_env_key="ha_onboarding_create_button_locator",
            description="계정 만들기 버튼",
        )

        if not create_clicked:
            logging.warning("계정 만들기 버튼을 클릭하지 못했습니다. 브라우저 상태를 확인하세요.")
            return False

        # 페이지 판별 후 위치(주소)/국가 단계 처리
        page_kind = _detect_current_page(driver)
        logging.info("현재 페이지 판별 결과: %s", page_kind)
        if page_kind == "onboarding_location":
            address_query = ensure_env_var_completed_2025_11_24(
                key_name="ha_onboarding_address_search_text",
                func_n="ensure_home_assistant_onboarding_completed",
                guide_text="Home Assistant 주소 검색에 사용할 값을 입력하세요 (예: 관평로 333):",
            )
            if not _handle_location_step(driver, wait, address_query, ha_url):
                logging.warning("주소 입력 단계 자동화가 완료되지 않았습니다.")
                return False
        elif page_kind == "onboarding_country":
            if not _handle_country_step(driver, wait, ha_url):
                logging.warning("국가 설정 단계 자동화가 완료되지 않았습니다.")
                return False
        elif page_kind == "onboarding_help":
            if not _handle_help_us_page(driver, wait, ha_url):
                logging.warning("도움 페이지 단계 자동화가 완료되지 않았습니다.")
                return False
        elif page_kind == "onboarding_ready":
            if not _handle_ready_page(driver, wait, ha_url):
                logging.warning("준비 완료 페이지 단계 자동화가 완료되지 않았습니다.")
                return False

        # 로그인 페이지 자동 확인 및 로그인 수행
        if not _handle_login_step(
            driver=driver,
            wait=wait,
            user_name=ha_user_name,
            password=ha_password,
            ha_url=ha_url,
        ):
            logging.warning("로그인 단계 자동화가 완료되지 않았습니다.")
            return False

        logging.info("온보딩 자동화가 로그인 단계까지 완료되었습니다.")
        return True

    except Exception as exc:
        logging.error("Home Assistant 온보딩 자동화 중 오류 발생: %s", exc, exc_info=True)
        if driver:
            _debug_dump_dom(driver.page_source, step="exception")
        return False
    finally:
        # headless_mode가 False인 경우 드라이버를 전역 변수에 유지하여 재사용 가능하게 함
        # headless_mode가 True인 경우에만 드라이버를 닫음
        if driver and headless_mode:
            try:
                driver.quit()
            except Exception:
                pass
        # headless_mode=False인 경우 드라이버는 전역 변수에 유지되므로 여기서 닫지 않음


@ensure_seconds_measured
def _needs_onboarding(html: str) -> bool:
    """Return True if onboarding screen likely present based on text/inputs."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        button_texts = [
            "나만의 스마트 홈 만들기",
            "Create my smart home",
            "계정 만들기",
            "Create account",
        ]
        text_found = any(
            soup.find(string=lambda text: text and candidate in text)
            for candidate in button_texts
        )
        input_present = bool(soup.select("input[name='username']"))
        return text_found or input_present
    except Exception as parse_error:
        logging.debug("온보딩 DOM 파싱 실패: %s", parse_error)
        return False


@ensure_seconds_measured
def _click_button_if_present(
    driver,
    wait: WebDriverWait,
    *,
    button_text_candidates: List[str],
    description: str,
    env_key: Optional[str] = None,
) -> None:
    """Click a button by text or cached/analyzed locator with fallbacks."""
    logging.debug("[onboarding-state] DOM 분석을 시작합니다.")
    _update_locator_cache_from_html(driver.page_source)
    _update_locator_cache_from_live_dom(driver)
    if env_key and env_key in _LOCATOR_CACHE:
        locator = _LOCATOR_CACHE[env_key]
        if _try_click_locator(driver, wait, locator, description, note="cached"):
            return

    for text_value in button_text_candidates:
        try:
            button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//button[contains(normalize-space(.), '{text_value}')]",
                    )
                )
            )
            button.click()
            logging.info("%s 클릭: %s", description, text_value)
            ensure_slept(milliseconds=500)
            return
        except TimeoutException:
            continue
        except Exception as exc:
            logging.debug("%s 클릭 중 예외(%s): %s", description, text_value, exc)
    _update_locator_cache_from_html(driver.page_source)
    if env_key and env_key in _LOCATOR_CACHE:
        locator = _LOCATOR_CACHE[env_key]
        if _try_click_locator(driver, wait, locator, description, note="analyzed"):
            return
    if env_key:
        locator = _get_or_request_locator(
            env_key=env_key,
            description=f"{description} locator (css:, xpath:, text:...)",
        )
        if locator:
            if _try_click_locator(driver, wait, locator, description, note="custom"):
                return
    logging.debug("%s 후보 버튼을 찾지 못했습니다: %s", description, button_text_candidates)


@ensure_seconds_measured
def _fill_onboarding_form(
    *,
    driver,
    wait: WebDriverWait,
    full_name: str,
    user_name: str,
    password: str,
    password_confirm: str,
) -> None:
    """Fill onboarding form fields (name, username, password, confirm) with shadow DOM support."""
    _update_locator_cache_from_html(driver.page_source)
    def _wait_for_form_ready():
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "input[name='name'], input[name='username']")
            )
            logging.debug("[onboarding-state] 입력 폼이 렌더링되었습니다.")
        except TimeoutException:
            logging.debug("[onboarding-state] 입력 폼 렌더링 대기 시간 초과.")
            _debug_dump_dom(driver.page_source, step="form-wait-timeout")

    _wait_for_form_ready()

    field_map = [
        {
            "selector": "input[name='name']",
            "fallback_selectors": [
                "input.mdc-text-field__input[name='name']",
                "ha-textfield[name='name']",
                "ha-textfield[label*='이름']",
                "mwc-textfield[name='name']",
                "mwc-textfield[label*='이름']",
                "ha-textfield[label*='Name']",
                "mwc-textfield[label*='Name']",
            ],
            "value": full_name,
            "description": "계정 표시 이름 입력 필드",
            "env_key": "ha_onboarding_selector_name",
        },
        {
            "selector": "input[name='username']",
            "fallback_selectors": [
                "input.mdc-text-field__input[name='username']",
                "ha-textfield[name='username']",
                "ha-textfield[label*='사용자']",
                "mwc-textfield[name='username']",
                "mwc-textfield[label*='사용자']",
                "ha-textfield[label*='Username']",
                "mwc-textfield[label*='Username']",
            ],
            "value": user_name,
            "description": "사용자 이름 입력 필드",
            "env_key": "ha_onboarding_selector_username",
        },
        {
            "selector": "input[name='password']",
            "fallback_selectors": [
                "input.mdc-text-field__input[name='password']",
                "ha-password-field[name='password']",
                "ha-password-field[label*='비밀번호']",
                "ha-password-field[label*='Password']",
                "ha-textfield[type='password']",
                "mwc-textfield[type='password']",
            ],
            "value": password,
            "description": "비밀번호 입력 필드",
            "env_key": "ha_onboarding_selector_password",
        },
        {
            "selector": "input[name='passwordConfirm'], input[name='password_confirm']",
            "fallback_selectors": [
                "input.mdc-text-field__input[name='password_confirm']",
                "input.mdc-text-field__input[name='passwordConfirm']",
                "ha-password-field[name='passwordConfirm']",
                "ha-password-field[name='password_confirm']",
                "ha-password-field[label*='확인']",
                "ha-password-field[label*='Confirm']",
                "mwc-textfield[name='passwordConfirm']",
                "mwc-textfield[name='password_confirm']",
                "mwc-textfield[label*='확인']",
            ],
            "value": password_confirm,
            "description": "비밀번호 확인 입력 필드",
            "env_key": "ha_onboarding_selector_password_confirm",
        },
    ]

    for field in field_map:
        selector = field["selector"]
        value = field["value"]
        description = field["description"]
        env_key = field["env_key"]
        fallback_selectors = field.get("fallback_selectors", [])

        filled = False
        logging.debug("필드(%s) Shadow DOM 우선 시도: %s", description, selector)
        if _fill_input_via_shadow(driver, selector, value):
            logging.debug("필드 입력 완료(Shadow DOM 1차): %s", selector)
            filled = True

        if filled:
            continue

        max_basic_attempts = 3
        for attempt in range(1, max_basic_attempts + 1):
            per_attempt_wait = WebDriverWait(driver, min(15, wait._timeout))
            logging.debug(
                "필드(%s) 기본 selector 시도 #%s/%s: %s",
                description,
                attempt,
                max_basic_attempts,
                selector,
            )
            _log_selector_presence(driver, selector, description, context="basic")
            try:
                element = per_attempt_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                element.clear()
                element.send_keys(value)
                logging.debug("필드 입력 완료: %s", selector)
                filled = True
                break
            except TimeoutException:
                logging.warning(
                    "필드(%s)를 기본 selector로 찾을 수 없습니다. (시도 %s/%s)",
                    selector,
                    attempt,
                    max_basic_attempts,
                )
            except Exception as exc:
                logging.error("필드(%s) 입력 중 오류: %s", selector, exc)
                raise

        if not filled:
            logging.warning("필드(%s)를 기본 selector로 찾지 못해 대체 selector를 시도합니다.", selector)
            for alt_selector in fallback_selectors:
                logging.debug("필드(%s) 대체 selector 시도: %s", description, alt_selector)
                _log_selector_presence(driver, alt_selector, description, context="fallback")
                if _fill_input_via_shadow(driver, alt_selector, value):
                    logging.debug("필드 입력 완료(Shadow DOM 대체 selector): %s", alt_selector)
                    filled = True
                    break
                if _fill_input_via_selector(driver, alt_selector, value):
                    logging.debug("필드 입력 완료(대체 selector): %s", alt_selector)
                    filled = True
                    break

        if filled:
            continue

        logging.warning("필드(%s)를 대체 selector로도 찾을 수 없습니다. locator 추론을 재시도합니다.", selector)
        start_time = time.time()
        custom_locator = None
        while (time.time() - start_time) < 30 and not custom_locator:
            custom_locator = _get_or_request_locator(
                env_key=env_key,
                description=f"{description} locator (css:, xpath:, text:...)",
                skip_prompt=True,
            )
            if custom_locator:
                break
            logging.debug("필드(%s) locator 자동 추론 재시도 중...", description)
            _update_locator_cache_from_live_dom(driver)
            time.sleep(1)

        if not custom_locator:
            custom_locator = _get_or_request_locator(
                env_key=env_key,
                description=f"{description} locator (css:, xpath:, text:...)",
            )
        if not custom_locator:
            _debug_dump_dom(driver.page_source, step=f"missing-{selector}")
            raise TimeoutException(f"필드({selector})에 대한 locator 를 찾을 수 없습니다.")

        logging.debug("필드(%s) 사용자 지정 locator 입력 시도: %s", description, custom_locator)
        element = wait.until(EC.presence_of_element_located(custom_locator))
        element.clear()
        element.send_keys(value)
        logging.debug("필드 입력 완료(사용자 지정 locator): %s", env_key)


@ensure_seconds_measured
def _fill_input_via_selector(driver, selector: str, value: str) -> bool:
    """Fill input by CSS selector by walking children and dispatching input/change events."""
    script = """
        const selector = arguments[0];
        const value = arguments[1];
        const root = document.querySelector(selector);
        if (!root) {
            return false;
        }

        function collectChildren(node) {
            if (!node) return [];
            if (node.children && node.children.length) {
                return Array.from(node.children);
            }
            if (node.childNodes && node.childNodes.length) {
                return Array.from(node.childNodes).filter(
                    (child) => child.nodeType === Node.ELEMENT_NODE
                );
            }
            return [];
        }

        function findInput(node) {
            if (!node) return null;
            if (node.nodeType === Node.ELEMENT_NODE && node.matches('input,textarea')) {
                return node;
            }
            if (node.shadowRoot) {
                const shadowFound = findInput(node.shadowRoot);
                if (shadowFound) {
                    return shadowFound;
                }
            }
            for (const child of collectChildren(node)) {
                const found = findInput(child);
                if (found) {
                    return found;
                }
            }
            return null;
        }

        const targetInput = findInput(root);
        if (!targetInput) {
            return false;
        }

        targetInput.focus();
        const descriptor = Object.getOwnPropertyDescriptor(
            Object.getPrototypeOf(targetInput),
            'value',
        );
        if (descriptor && descriptor.set) {
            descriptor.set.call(targetInput, '');
        } else {
            targetInput.value = '';
        }
        targetInput.dispatchEvent(new Event('input', { bubbles: true }));

        if (descriptor && descriptor.set) {
            descriptor.set.call(targetInput, value);
        } else {
            targetInput.value = value;
        }
        targetInput.dispatchEvent(new Event('input', { bubbles: true }));
        targetInput.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    """

    try:
        return bool(driver.execute_script(script, selector, value))
    except Exception as exc:
        logging.debug("selector(%s) 입력 시도 중 오류: %s", selector, exc)
        return False


@ensure_seconds_measured
def _fill_input_via_shadow(driver, selector: str, value: str) -> bool:
    """Fill input inside shadow DOM host selected by selector; log host/input paths."""
    script = """
        const selector = arguments[0];
        const value = arguments[1];
        function normalizeTag(node) {
            if (!node) return '<null>';
            if (node.tagName) return node.tagName.toLowerCase();
            if (node === document) return 'document';
            if (node.nodeType === Node.DOCUMENT_FRAGMENT_NODE) return '#shadow-root';
            return '<node>';
        }

        function findHost(node, selector, path) {
            if (!node) return null;
            if (node.nodeType === Node.ELEMENT_NODE && node.matches && node.matches(selector)) {
                return { element: node, path: path.concat(normalizeTag(node)) };
            }
            if (node.shadowRoot) {
                const shadowResult = findHost(
                    node.shadowRoot,
                    selector,
                    path.concat(normalizeTag(node) + '#shadow'),
                );
                if (shadowResult) {
                    return shadowResult;
                }
            }
            const children = node.children
                ? Array.from(node.children)
                : Array.from(node.childNodes || []).filter(
                      (child) => child.nodeType === Node.ELEMENT_NODE,
                  );
            for (const child of children) {
                const childResult = findHost(child, selector, path.concat(normalizeTag(child)));
                if (childResult) {
                    return childResult;
                }
            }
            return null;
        }

        function findInput(node, path) {
            if (!node) return null;
            if (node.nodeType === Node.ELEMENT_NODE && node.matches('input,textarea')) {
                return { element: node, path };
            }
            if (node.shadowRoot) {
                const shadowResult = findInput(node.shadowRoot, path.concat(node.tagName + '#shadow'));
                if (shadowResult) {
                    return shadowResult;
                }
            }
            const children = node.children
                ? Array.from(node.children)
                : Array.from(node.childNodes || []).filter(
                      (child) => child.nodeType === Node.ELEMENT_NODE,
                  );
            for (const child of children) {
                const childResult = findInput(child, path.concat(child.tagName));
                if (childResult) {
                    return childResult;
                }
            }
            return null;
        }

        const hostResult = findHost(document.body, selector, ['document.body']);
        if (!hostResult) {
            return { success: false, reason: 'host-not-found' };
        }

        const result = findInput(hostResult.element, hostResult.path);
        if (!result) {
            return { success: false, reason: 'input-not-found' };
        }

        const targetInput = result.element;
        targetInput.focus();
        const descriptor = Object.getOwnPropertyDescriptor(
            Object.getPrototypeOf(targetInput),
            'value',
        );
        if (descriptor && descriptor.set) {
            descriptor.set.call(targetInput, '');
        } else {
            targetInput.value = '';
        }
        targetInput.dispatchEvent(new Event('input', { bubbles: true }));

        if (descriptor && descriptor.set) {
            descriptor.set.call(targetInput, value);
        } else {
            targetInput.value = value;
        }
        targetInput.dispatchEvent(new Event('input', { bubbles: true }));
        targetInput.dispatchEvent(new Event('change', { bubbles: true }));
        return {
            success: true,
            path: result.path.join(' > '),
            tag: targetInput.tagName,
            hasShadowRoot: !!targetInput.shadowRoot,
            selectorUsed: selector,
            hostPath: hostResult.path.join(' > '),
        };
    """

    try:
        result = driver.execute_script(script, selector, value)
        if isinstance(result, dict):
            if result.get("success"):
                logging.debug(
                    "selector(%s) shadow DOM 입력 성공: tag=%s hostPath=%s inputPath=%s",
                    selector,
                    result.get("tag"),
                    result.get("hostPath"),
                    result.get("path"),
                )
                return True
            logging.debug(
                "selector(%s) shadow DOM 입력 실패 이유=%s",
                selector,
                result.get("reason"),
            )
            return False
        return bool(result)
    except Exception as exc:
        logging.debug("selector(%s) shadow DOM 입력 시도 중 오류: %s", selector, exc)
        return False


@ensure_seconds_measured
def _log_selector_presence(driver, selector: str, description: str, *, context: str) -> None:
    """Log shallow/deep match counts for a selector to aid debugging."""
    try:
        shallow, deep = _get_selector_counts(driver, selector)
        logging.debug(
            "[selector-check][%s] %s selector '%s' 매칭 개수 shallow=%s deep=%s",
            context,
            description,
            selector,
            shallow,
            deep,
        )
    except Exception as exc:
        logging.debug(
            "[selector-check][%s] %s selector '%s' 확인 실패: %s",
            context,
            description,
            selector,
            exc,
        )

@ensure_seconds_measured
def _get_selector_counts(driver, selector: str) -> Tuple[int, int]:
    script = """
        const selector = arguments[0];
        const shallow = document.querySelectorAll(selector).length;

        function search(node) {
            let count = 0;
            if (node.nodeType === Node.ELEMENT_NODE && node.matches && node.matches(selector)) {
                count += 1;
            }
            if (node.shadowRoot) {
                count += search(node.shadowRoot);
            }
            const children = node.children
                ? Array.from(node.children)
                : Array.from(node.childNodes || []).filter(
                      (child) => child.nodeType === Node.ELEMENT_NODE,
                  );
            for (const child of children) {
                count += search(child);
            }
            return count;
        }

        const deep = search(document.body);
        return { shallow, deep };
    """
    try:
        result = driver.execute_script(script, selector)
        if isinstance(result, dict):
            return int(result.get("shallow", 0)), int(result.get("deep", 0))
        # Fallback: if not dict, treat as shallow count
        count = int(result) if result is not None else 0
        return count, count
    except Exception:
        return 0, 0

@ensure_seconds_measured
def _debug_dump_dom(html: Optional[str], *, step: str) -> None:
    """Save HTML snapshot and log parsed inputs/buttons for step."""
    if not html:
        logging.debug("[onboarding-dom][%s] html 비어있음", step)
        return
    try:
        snapshot_path = _save_dom_snapshot(html, step)
        soup = BeautifulSoup(html, "html.parser")
        inputs = [
            f"name={inp.get('name')} id={inp.get('id')} type={inp.get('type')} placeholder={inp.get('placeholder')}"
            for inp in soup.find_all("input")
        ]
        buttons = [
            " ".join(button.get_text(strip=True).split())
            for button in soup.find_all("button")
        ]
        logging.debug(
            "[onboarding-dom][%s] 입력 필드=%s 버튼=%s snapshot=%s",
            step,
            inputs,
            buttons,
            snapshot_path,
        )
        _analyze_onboarding_dom(soup, step=step, snapshot_path=snapshot_path)
    except Exception as exc:
        logging.debug("[onboarding-dom][%s] 파싱 실패: %s", step, exc)


_LOCATOR_CACHE: Dict[str, Tuple[By, str]] = {}

@ensure_seconds_measured
def _detect_current_page(driver) -> str:
    """Detect current HA page kind: login/onboarding_location/onboarding_country/onboarding_help/onboarding_ready/overview/unknown."""
    try:
        html = driver.page_source or ""
        current_url = driver.current_url or ""
        
        # 0) 인증 페이지 판별 (가장 먼저 확인)
        if "/auth/authorize" in current_url or "/auth" in current_url:
            return "auth"
        
        # 1) 로그인 페이지 판별
        shallow_u, deep_u = _get_selector_counts(driver, "input[name='username'], input.mdc-text-field__input[name='username']")
        shallow_p, deep_p = _get_selector_counts(driver, "input[name='password'], input.mdc-text-field__input[name='password']")
        if ("집에 오신 것을 환영합니다" in html) or (deep_u > 0 and deep_p > 0):
            return "login"
        
        # 2) 둘러보기 페이지 판별 (온보딩 페이지 판별보다 먼저 확인)
        # 온보딩이 완료된 경우 둘러보기 페이지일 수 있으므로 먼저 확인
        if _is_overview_page(driver, html, current_url):
            return "overview"
        
        # 3) 위치 페이지 판별
        if _is_location_page(driver, html):
            return "onboarding_location"
        # 4) 국가 설정 페이지 판별
        if _is_country_page(driver, html):
            return "onboarding_country"
        # 5) 도움(telemetry/옵션) 페이지 판별
        if _is_help_us_page(driver, html):
            return "onboarding_help"
        # 6) 준비 완료 페이지 판별
        if _is_ready_page(driver, html):
            return "onboarding_ready"
        
        # 필요 시 다른 온보딩 단계 추가 확장 가능
        return "unknown"
    except Exception as exc:
        logging.debug("페이지 판별 중 예외: %s", exc)
        return "unknown"

@ensure_seconds_measured
def _is_location_page(driver, html: Optional[str] = None) -> bool:
    """Return True if current page looks like '집 위치' step."""
    text = (html or driver.page_source or "")
    # 텍스트 힌트들
    location_text_hints = [
        "집 위치", "Home location", "Your location", "Set location", "주소", "위치"
    ]
    if any(h in text for h in location_text_hints):
        return True
    # 컴포넌트/셀렉터 힌트들
    selectors = [
        "ha-onboarding-map",
        "ha-location-picker",
        "input[name='search']",
        "input[name='address']",
        "button.mdc-icon-button",
    ]
    for sel in selectors:
        _, deep = _get_selector_counts(driver, sel)
        if deep > 0:
            return True
    return False

@ensure_seconds_measured
def _is_country_page(driver, html: Optional[str] = None) -> bool:
    """Return True if current page looks like country selection step."""
    text = (html or driver.page_source or "")
    hints = [
        "올바른 단위를 사용할 수 있도록 귀하의 집이 있는 국가를 알고 싶습니다",
        "국가",
        "Country",
    ]
    if any(h in text for h in hints):
        return True
    # 구조적 힌트: mdc select anchor / selected text
    selectors = [
        ".mdc-select__anchor",
        ".mdc-select__selected-text",
        "mwc-select",
    ]
    for sel in selectors:
        _, deep = _get_selector_counts(driver, sel)
        if deep > 0:
            return True
    return False

@ensure_seconds_measured
def _is_help_us_page(driver, html: Optional[str] = None) -> bool:
    """Return True if current page looks like 'help us help you' step."""
    text = (html or driver.page_source or "")
    hints = [
        "우리가 당신을 도울 수 있도록 도와주세요",
        "Help us help you",
    ]
    if any(h in text for h in hints):
        return True
    # 흔히 다음 버튼만 있는 단일 카드 형식
    _, deep_next = _get_selector_counts(driver, "ha-button, button.button.has-label")
    return deep_next > 0

@ensure_seconds_measured
def _is_ready_page(driver, html: Optional[str] = None) -> bool:
    """Return True if current page looks like '준비 완료!' step."""
    text = (html or driver.page_source or "")
    hints = [
        "준비 완료!",
        "You're all set",
        "All set",
    ]
    if any(h in text for h in hints):
        return True
    # 다음 버튼 유무로도 보조 판별
    _, deep_btn = _get_selector_counts(driver, "ha-button > button.button.has-label, button.button.has-label")
    return deep_btn > 0

@ensure_seconds_measured
def _is_overview_page(driver, html: Optional[str] = None, current_url: Optional[str] = None) -> bool:
    """Return True if current page looks like Home Assistant overview (둘러보기) page.
    
    판별 기준: 
    1. URL이 /lovelace/0 또는 / (둘러보기 페이지)
    2. <div class="main-title">둘러보기</div> 요소의 존재 여부
    3. "Add to Home Assistant" 버튼 존재 여부
    """
    try:
        # URL 기반 사전 필터링: 인증/온보딩 페이지는 둘러보기가 아님
        if current_url is None:
            try:
                current_url = driver.current_url or ""
            except Exception:
                current_url = ""
        
        if "/auth" in current_url or "/onboarding" in current_url.lower():
            logging.debug("둘러보기 페이지 아님: URL에 /auth 또는 /onboarding 포함 (%s)", current_url)
            return False
        
        # URL 기반 판별: /lovelace/0 또는 / 는 둘러보기 페이지일 가능성이 높음
        # (단, 온보딩 페이지가 아닌 경우에만)
        if current_url:
            url_normalized = current_url.rstrip("/")
            if url_normalized.endswith(":8123") or url_normalized.endswith(":8123/") or "/lovelace/0" in current_url:
                # 온보딩 페이지가 아닌지 확인
                if not ("집 위치" in (html or driver.page_source or "") or "onboarding" in current_url.lower()):
                    logging.info("둘러보기 페이지 확인됨: URL 기반 판별 (URL: %s)", current_url)
                    return True
        
        # 둘러보기 페이지의 명확한 표시: <div class="main-title">둘러보기</div>
        # Shadow DOM을 포함하여 검색
        js_check = """
        function findOverviewTitle() {
            // 일반 DOM에서 검색
            const mainTitle = document.querySelector('div.main-title');
            if (mainTitle && mainTitle.textContent && mainTitle.textContent.trim().includes('둘러보기')) {
                return true;
            }
            
            // Shadow DOM에서도 검색
            const allElements = document.querySelectorAll('*');
            for (const el of allElements) {
                if (el.shadowRoot) {
                    const shadowTitle = el.shadowRoot.querySelector('div.main-title');
                    if (shadowTitle && shadowTitle.textContent && shadowTitle.textContent.trim().includes('둘러보기')) {
                        return true;
                    }
                }
            }
            return false;
        }
        return findOverviewTitle();
        """
        result = driver.execute_script(js_check)
        if result:
            logging.info("둘러보기 페이지 확인됨: <div class='main-title'>둘러보기</div> 요소 발견 (URL: %s)", current_url)
            return True
        
        # 대체 방법: CSS selector로 직접 검색 (Shadow DOM 포함)
        _, deep_count = _get_selector_counts(
            driver,
            "div.main-title"
        )
        if deep_count > 0:
            # 텍스트 내용 확인
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, "div.main-title")
                for elem in elements:
                    text = elem.text or ""
                    if "둘러보기" in text:
                        logging.info("둘러보기 페이지 확인됨: div.main-title에 '둘러보기' 텍스트 발견 (URL: %s)", current_url)
                        return True
            except Exception as e:
                logging.debug("div.main-title 요소 텍스트 확인 중 오류: %s", e)
        
        # 추가 판별: "Add to Home Assistant" 버튼이 있으면 둘러보기 페이지일 가능성이 높음
        _, deep_add_button = _get_selector_counts(
            driver, 
            "button[aria-label*='Add to Home Assistant'], mwc-icon-button[aria-label*='Add to Home Assistant']"
        )
        if deep_add_button > 0:
            # 온보딩 페이지가 아닌지 확인
            if not ("집 위치" in (html or driver.page_source or "") or "onboarding" in current_url.lower()):
                logging.info("둘러보기 페이지 확인됨: 'Add to Home Assistant' 버튼 발견 (URL: %s)", current_url)
                return True
        
        logging.debug("둘러보기 페이지가 아닙니다: <div class='main-title'>둘러보기</div> 요소를 찾을 수 없습니다. (URL: %s)", current_url)
        return False
    except Exception as exc:
        logging.debug("둘러보기 페이지 판별 중 오류: %s (URL: %s)", exc, current_url)
        return False

@ensure_seconds_measured
def _is_location_permission_dialog_present(driver) -> bool:
    """Return True if location permission dialog/alert likely visible."""
    try:
        # 1) DOM/Shadow 기반 다이얼로그 탐지 우선
        html = driver.page_source or ""
        hint_texts = [
            "귀하의 위치", "현재 위치", "위치 접근", "위치 권한",
            "Allow Home Assistant to access your location",
            "Use your current location",
            "귀하의 위치를 감지하기를 원하십니까?",
        ]
        if any(h in html for h in hint_texts):
            return True
        # 다이얼로그/버튼 구조 힌트
        selectors = [
            "ha-dialog",
            "[role='dialog']",
            "dialog[role='alertdialog']",
            "ha-dialog button.button.has-label",
            "ha-button > button.button.has-label",
            "mwc-dialog",
            "ha-alert-dialog",
            "dialog-box",
            "ha-md-dialog",
        ]
        for sel in selectors:
            _, deep = _get_selector_counts(driver, sel)
            if deep > 0:
                return True
        # 2) 브라우저 alert 존재 여부 (fallback)
        try:
            _ = driver.switch_to.alert
            return True
        except Exception:
            pass
        return False
    except Exception:
        return False

@ensure_seconds_measured
def _wait_until_location_permission_dialog_present(driver, max_wait_seconds: int = 8) -> bool:
    """Wait until location permission dialog becomes visible or timeout."""
    start = time.time()
    while (time.time() - start) < max_wait_seconds:
        if _is_location_permission_dialog_present(driver):
            return True
        ensure_slept(milliseconds=200)
    return _is_location_permission_dialog_present(driver)

@ensure_seconds_measured
def _try_grant_geolocation_permission(driver, ha_url: str) -> None:
    """Grant geolocation permission via CDP to bypass browser permission dialog."""
    try:
        origin = ha_url.rstrip("/")
        # Selenium 4: execute_cdp_cmd available on Chromium drivers
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {"origin": origin, "permissions": ["geolocation"]},
        )
        logging.info("CDP를 통해 지리적 위치 권한을 사전 승인했습니다: origin=%s", origin)
    except Exception as exc:
        logging.debug("CDP 지리적 위치 권한 승인 실패(무시 가능): %s", exc)

@ensure_seconds_measured
def _log_pre_connection_diagnostics(driver, target_url: str) -> None:
    """Log page diagnostics (URL, title, readyState, key markers) right after navigation."""
    try:
        current_url = driver.current_url
        title = driver.title
        ready_state = driver.execute_script("return document.readyState;")
        has_onboarding = "onboarding" in (current_url.lower() + " " + (driver.page_source or "").lower())
        logging.info("사전 진단: current_url=%s title=%s readyState=%s onboarding_hint=%s",
                     current_url, title, ready_state, has_onboarding)
    except Exception as exc:
        logging.debug("사전 진단 수집 실패: %s", exc)

@ensure_seconds_measured
def _click_primary_button_in_dialog(driver) -> bool:
    """Click primary button inside visible dialog containers when text-based click fails."""
    script = """
        function findDeep(root, selector) {
            function search(node){
                if(!node) return null;
                try{ if(node.matches && node.matches(selector)) return node; }catch(e){}
                if(node.shadowRoot){
                    const s = search(node.shadowRoot);
                    if(s) return s;
                }
                const kids = node.children ? Array.from(node.children)
                    : Array.from(node.childNodes||[]).filter(n=>n.nodeType===Node.ELEMENT_NODE);
                for(const k of kids){
                    const s = search(k);
                    if(s) return s;
                }
                return null;
            }
            return search(root||document.body);
        }
        function findAllDeep(root, selector) {
            const results = [];
            function search(node){
                if(!node) return;
                try{ if(node.matches && node.matches(selector)) results.push(node); }catch(e){}
                if(node.shadowRoot) search(node.shadowRoot);
                const kids = node.children ? Array.from(node.children)
                    : Array.from(node.childNodes||[]).filter(n=>n.nodeType===Node.ELEMENT_NODE);
                for(const k of kids) search(k);
            }
            search(root||document.body);
            return results;
        }
        const containers = [
            'ha-dialog', '[role=\"dialog\"]', 'mwc-dialog', 'ha-alert-dialog'
        ];
        let container = null;
        for (const c of containers) {
            const found = findDeep(document.body, c);
            if (found) { container = found; break; }
        }
        if (!container) return false;
        const buttons = findAllDeep(container, 'button.button.has-label, ha-button > button.button.has-label, button');
        if (!buttons.length) return false;
        // Prefer enabled, visible button
        const visible = buttons.find(b => !!(b.offsetWidth || b.offsetHeight || b.getClientRects().length));
        const btn = visible || buttons[0];
        try { btn.click(); return true; } catch(e) {}
        try { btn.dispatchEvent(new MouseEvent('click', {bubbles:true,cancelable:true})); return true; } catch(e) {}
        return false;
    """
    try:
        return bool(driver.execute_script(script))
    except Exception:
        return False

@ensure_seconds_measured
def _click_dialog_ok_via_structure(driver) -> bool:
    """Click OK in dialog-box/ha-md-dialog structure: prefer autofocus OK or last action."""
    script = """
        function findAllDeep(root, selector) {
            const results = [];
            function search(node){
                if(!node) return;
                try{ if(node.matches && node.matches(selector)) results.push(node); }catch(e){}
                if(node.shadowRoot) search(node.shadowRoot);
                const kids = node.children ? Array.from(node.children)
                    : Array.from(node.childNodes||[]).filter(n=>n.nodeType===Node.ELEMENT_NODE);
                for(const k of kids) search(k);
            }
            search(root||document.body);
            return results;
        }
        function clickInnerButton(host) {
            // Prefer ha-button[autofocus]
            const autofocus = findAllDeep(host, "ha-button[autofocus] > button.button.has-label");
            if (autofocus.length) {
                try { autofocus[0].click(); return true; } catch(e) {}
            }
            // Fallback: actions slot last ha-button
            const actionButtons = findAllDeep(host, "slot[name='actions'], .actions");
            if (actionButtons.length) {
                // collect buttons under actions
                const btns = findAllDeep(actionButtons[0], "ha-button > button.button.has-label, button.button.has-label");
                const visible = btns.filter(b => !!(b.offsetWidth || b.offsetHeight || b.getClientRects().length));
                const target = (visible.length ? visible[visible.length - 1] : (btns[btns.length - 1] || null));
                if (target) {
                    try { target.click(); return true; } catch(e) {}
                }
            }
            // As last resort, any visible button in dialog
            const any = findAllDeep(host, "button");
            for (const b of any) {
                if (!!(b.offsetWidth || b.offsetHeight || b.getClientRects().length)) {
                    try { b.click(); return true; } catch(e) {}
                }
            }
            return false;
        }
        const containers = ["dialog-box", "ha-md-dialog", "dialog[role='alertdialog']"];
        for (const sel of containers) {
            const hosts = findAllDeep(document.body, sel);
            for (const h of hosts) {
                if (clickInnerButton(h)) return true;
            }
        }
        return false;
    """
    try:
        return bool(driver.execute_script(script))
    except Exception:
        return False

@ensure_seconds_measured
def _handle_help_us_page(
    driver,
    wait: WebDriverWait,
    ha_url: str,
) -> bool:
    """Handle 'Help us help you' step by clicking Next."""
    logging.info("도움(Help us help you) 페이지 단계를 자동화합니다.")
    if not _is_help_us_page(driver):
        logging.info("도움 페이지로 감지되지 않아 단계를 건너뜁니다.")
        return True
    # 위치 권한 다이얼로그가 이 단계에서 늦게 나타나는 경우도 처리
    if _is_location_permission_dialog_present(driver):
        # 텍스트 → 구조 → 기본 버튼 → alert 순으로 시도
        ok_texts = ["OK", "확인", "허용", "Allow"]
        for t in ok_texts:
            if _click_by_text_deep(driver, t):
                ensure_slept(milliseconds=300)
                break
        else:
            selectors = [
                "ha-dialog button.button.has-label",
                "ha-button > button.button.has-label",
                "button.button.has-label",
                "[role='dialog'] button.button.has-label",
                "dialog-box ha-button[autofocus] > button.button.has-label",
                "ha-md-dialog ha-button[autofocus] > button.button.has-label",
            ]
            if not _click_element_via_shadow(driver, selectors, "권한 다이얼로그 OK 버튼(도움 단계)"):
                if not (_click_dialog_ok_via_structure(driver) or _click_primary_button_in_dialog(driver)):
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                        ensure_slept(milliseconds=300)
                    except Exception:
                        pass
    # 다음 클릭
    if _click_by_text_deep(driver, "다음") or _click_by_text_deep(driver, "Next"):
        ensure_slept(milliseconds=500)
        return True
    if _click_element_via_shadow(driver, ["ha-button > button.button.has-label", "button.button.has-label"], "다음 버튼(도움 단계)"):
        ensure_slept(milliseconds=500)
        return True
    logging.warning("도움 페이지 단계에서 다음 버튼 클릭 실패")
    return False

@ensure_seconds_measured
def _handle_ready_page(
    driver,
    wait: WebDriverWait,
    ha_url: str,
) -> bool:
    """Handle '준비 완료!' step by clicking the primary Next button."""
    logging.info("준비 완료 페이지 단계를 자동화합니다.")
    if not _is_ready_page(driver):
        logging.info("준비 완료 페이지로 감지되지 않아 단계를 건너뜁니다.")
        return True
    # 다이얼로그가 남아있다면 먼저 처리
    if _is_location_permission_dialog_present(driver):
        if not (_click_dialog_ok_via_structure(driver) or _click_primary_button_in_dialog(driver) or _click_by_text_deep(driver, "OK")):
            try:
                alert = driver.switch_to.alert
                alert.accept()
                ensure_slept(milliseconds=300)
            except Exception:
                pass
    # 버튼 구조 기반 클릭
    if _click_element_via_shadow(driver, ["ha-button > button.button.has-label", "button.button.has-label"], "다음 버튼(준비 완료)"):
        ensure_slept(milliseconds=500)
        return True
    # 텍스트 기반 보조
    if _click_by_text_deep(driver, "다음") or _click_by_text_deep(driver, "Next"):
        ensure_slept(milliseconds=500)
        return True
    logging.warning("준비 완료 페이지에서 다음 버튼 클릭 실패")
    return False

@ensure_seconds_measured
def _get_or_request_locator(
    env_key: str,
    description: str,
    *,
    skip_prompt: bool = False,
) -> Optional[Tuple[By, str]]:
    """Get locator from cache/env or prompt (unless skip_prompt)."""
    if not env_key:
        return None
    if env_key in _LOCATOR_CACHE:
        return _LOCATOR_CACHE[env_key]

    raw_value = os.environ.get(env_key)
    if not raw_value and not skip_prompt:
        raw_value = ensure_env_var_completed_2025_11_24(
            key_name=env_key,
            func_n="ensure_home_assistant_onboarding_completed",
            guide_text=(
                f"{description}를 입력하세요.\n"
                "형식 예시:\n"
                "  css:button[data-test='start']\n"
                "  xpath://button[contains(., '계정 만들기')]\n"
                "  text:계정 만들기\n"
            ),
        )
    if not raw_value:
        return None

    locator = _locator_from_string(raw_value)
    if locator:
        _LOCATOR_CACHE[env_key] = locator
    return locator


@ensure_seconds_measured
def _locator_from_string(raw_value: Optional[str]) -> Optional[Tuple[By, str]]:
    """Parse 'css:', 'xpath:', or 'text:' into a (By, value) locator tuple."""
    if not raw_value:
        return None

    value = raw_value.strip()
    lower = value.lower()

    if lower.startswith("css:"):
        return By.CSS_SELECTOR, value[4:].strip()
    if lower.startswith("xpath:"):
        return By.XPATH, value[6:].strip()
    if lower.startswith("text:"):
        text = value[5:].strip()
        xpath = f"//*[contains(normalize-space(.), '{text}')]"
        return By.XPATH, xpath

    # 기본값은 CSS selector로 간주
    return By.CSS_SELECTOR, value


@ensure_seconds_measured
def _try_click_locator(driver, wait, locator: Tuple[By, str], description: str, note: str) -> bool:
    """Try clicking a locator with wait; return True on success."""
    try:
        button = wait.until(EC.element_to_be_clickable(locator))
        button.click()
        logging.info("%s 클릭 (%s locator=%s)", description, note, locator)
        ensure_slept(milliseconds=500)
        return True
    except TimeoutException:
        logging.warning("%s locator 클릭 실패(Timeout) [%s]", description, note)
    except Exception as exc:
        logging.warning("%s locator 클릭 실패 [%s]: %s", description, note, exc)
    return False


@ensure_seconds_measured
def _update_locator_cache_from_html(html: str) -> None:
    """Analyze current HTML (non-shadow) to recommend and cache locators."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        _analyze_onboarding_dom(soup, step="runtime-update", snapshot_path=None)
        logging.debug("[onboarding-state] runtime DOM 분석 완료")
    except Exception as exc:
        logging.debug("runtime DOM 분석 실패: %s", exc)


@ensure_seconds_measured
def _update_locator_cache_from_live_dom(driver) -> None:
    """Traverse DOM + shadow roots to collect inputs/buttons; cache locator recommendations."""
    logging.debug("[onboarding-live] shadow DOM 포함 locator 추론을 시작합니다.")
    script = """
        function normalize(text) {
            if (!text) return '';
            return text.replace(/\\s+/g, ' ').trim();
        }

        function collectElements(root) {
            const stack = [root];
            const buttons = [];
            const inputs = [];

            while (stack.length) {
                const node = stack.pop();
                if (!node) continue;

                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches('button, ha-button, mwc-button')) {
                        buttons.push({
                            text: normalize(node.textContent),
                            tag: node.tagName.toLowerCase(),
                        });
                    }
                    if (node.matches('input')) {
                        inputs.push({
                            name: node.getAttribute('name'),
                            id: node.id,
                            type: node.type,
                            placeholder: node.getAttribute('placeholder'),
                        });
                    }
                }

                if (node.shadowRoot) {
                    stack.push(node.shadowRoot);
                }

                const children = node.children
                    ? Array.from(node.children)
                    : Array.from(node.childNodes || []).filter(
                          (child) => child.nodeType === Node.ELEMENT_NODE,
                      );
                for (const child of children) {
                    stack.push(child);
                }
            }

            return { buttons, inputs };
        }

        return collectElements(document.body);
    """

    try:
        result = driver.execute_script(script)
    except Exception as exc:
        logging.debug("[onboarding-live] shadow DOM 분석 스크립트 실패: %s", exc)
        return

    if not result:
        logging.debug("[onboarding-live] shadow DOM 분석 결과가 비어 있습니다.")
        return

    buttons = result.get("buttons", [])
    inputs = result.get("inputs", [])
    logging.debug(
        "[onboarding-live] shadow DOM 버튼=%s 입력필드=%s",
        buttons,
        inputs,
    )

    recommendations: Dict[str, str] = {}

    for button in buttons:
        text = button.get("text")
        if not text:
            continue
        if "나만의 스마트 홈 만들기" in text:
            recommendations["ha_onboarding_start_button_locator"] = f"text:{text}"
        if "계정 만들기" in text or "Create account" in text:
            recommendations["ha_onboarding_create_button_locator"] = f"text:{text}"

    for field in inputs:
        name = (field.get("name") or "").strip()
        placeholder = (field.get("placeholder") or "").lower()
        if name == "name" or "이름" in placeholder:
            recommendations["ha_onboarding_selector_name"] = "css:input[name='name']"
        if name == "username" or "사용자" in placeholder:
            recommendations["ha_onboarding_selector_username"] = "css:input[name='username']"
        if name == "username" or "사용자" in placeholder:
            recommendations["ha_onboarding_selector_username"] = "css:input[name='username']"
        if name == "password" and "확인" not in placeholder:
            recommendations["ha_onboarding_selector_password"] = "css:input[name='password']"
        if name == "passwordConfirm" or ("확인" in placeholder and not name):
            recommendations["ha_onboarding_selector_password_confirm"] = "css:input[name='passwordConfirm']"
        if name == "password_confirm":
            recommendations["ha_onboarding_selector_password_confirm"] = "css:input[name='password_confirm']"
        if "확인" in placeholder and "password" in name:
            recommendations.setdefault(
                "ha_onboarding_selector_password_confirm",
                "css:input[name='passwordConfirm']",
            )

    if recommendations:
        logging.info("[onboarding-live] shadow DOM 기반 locator 추천=%s", recommendations)
        for env_key, locator in recommendations.items():
            parsed = _locator_from_string(locator)
            if parsed and env_key not in _LOCATOR_CACHE:
                _LOCATOR_CACHE[env_key] = parsed
    else:
        logging.debug("[onboarding-live] shadow DOM 기반 추천 locator 가 없습니다.")

@ensure_seconds_measured
def _save_dom_snapshot(html: str, step: str) -> Path:
    """Save DOM snapshot to pk_logs/selenium; fallback to temp dir on permission error."""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
    primary_dir = d_pk_logs / "selenium"
    fallback_dir = Path(tempfile.gettempdir()) / "pk_system" / "selenium"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"ha_onboarding_{step}_{timestamp}.html"

    for directory in (primary_dir, fallback_dir):
        try:
            directory.mkdir(parents=True, exist_ok=True)
            file_path = directory / filename
            file_path.write_text(html, encoding="utf-8")
            return file_path
        except PermissionError as exc:
            logging.warning(
                "[onboarding-dom] %s 디렉터리에 스냅샷 저장 실패(%s). 다음 경로를 시도합니다.",
                directory,
                exc,
            )
            continue
        except Exception as exc:
            logging.warning(
                "[onboarding-dom] %s 디렉터리에 스냅샷 저장 중 오류: %s",
                directory,
                exc,
            )
            continue

    logging.error("[onboarding-dom] 모든 경로에 스냅샷 저장 실패.")
    return Path("")


@ensure_seconds_measured
def _analyze_onboarding_dom(soup: BeautifulSoup, *, step: str, snapshot_path: Path) -> None:
    """Analyze parsed HTML for button texts and input fields; cache locator hints."""
    try:
        button_texts = [
            (" ".join(btn.get_text(strip=True).split()), btn)
            for btn in soup.find_all("button")
        ]
        input_fields = [
            {
                "name": inp.get("name"),
                "id": inp.get("id"),
                "placeholder": inp.get("placeholder"),
                "type": inp.get("type"),
            }
            for inp in soup.find_all("input")
        ]

        logging.debug(
            "[onboarding-analyze][%s] 버튼=%s 필드=%s snapshot=%s",
            step,
            [text for text, _ in button_texts],
            input_fields,
            snapshot_path,
        )

        recommendations: Dict[str, str] = {}

        for text, _ in button_texts:
            if text:
                normalized = text.strip()
                if "나만의 스마트 홈 만들기" in normalized:
                    recommendations["ha_onboarding_start_button_locator"] = f"text:{normalized}"
                if "계정 만들기" in normalized or "Create account" in normalized:
                    recommendations["ha_onboarding_create_button_locator"] = f"text:{normalized}"

        for field in input_fields:
            name = field.get("name")
            placeholder = (field.get("placeholder") or "").lower()
            if name == "name" or "이름" in placeholder:
                recommendations["ha_onboarding_selector_name"] = "css:input[name='name']"
            if name == "username" or "사용자 이름" in placeholder:
                recommendations["ha_onboarding_selector_username"] = "css:input[name='username']"
            if name == "password" and "확인" not in placeholder:
                recommendations["ha_onboarding_selector_password"] = "css:input[name='password']"
            if name in {"password_confirm", "passwordConfirm"} or "확인" in placeholder:
                recommendations["ha_onboarding_selector_password_confirm"] = "css:input[name='passwordConfirm']"

        if recommendations:
            logging.info("[onboarding-analyze][%s] locator 추천=%s", step, recommendations)
            for env_key, locator in recommendations.items():
                _LOCATOR_CACHE.setdefault(env_key, _locator_from_string(locator))
    except Exception as exc:
        logging.debug("[onboarding-analyze][%s] 분석 실패: %s", step, exc)

@ensure_seconds_measured
def _click_element_via_shadow(driver, selectors: List[str], description: str) -> bool:
    """Click first element matching any selector across shadow DOM; return True if clicked."""
    script = """
        const selectors = arguments[0] || [];
        function findBySelectorDeep(selector) {
            function matches(node, sel) {
                try { return node.matches && node.matches(sel); } catch(e) { return false; }
            }
            function search(node, sel) {
                if (!node) return null;
                if (matches(node, sel)) return node;
                if (node.shadowRoot) {
                    const inside = search(node.shadowRoot, sel);
                    if (inside) return inside;
                }
                const kids = node.children
                    ? Array.from(node.children)
                    : Array.from(node.childNodes||[]).filter(n => n.nodeType === Node.ELEMENT_NODE);
                for (const k of kids) {
                    const r = search(k, sel);
                    if (r) return r;
                }
                return null;
            }
            return search(document.body, selector);
        }
        for (const sel of selectors) {
            const el = findBySelectorDeep(sel);
            if (el) {
                try { el.click(); return true; } catch(e) { /* ignore */ }
            }
        }
        return false;
    """
    try:
        ok = bool(driver.execute_script(script, selectors))
        if ok:
            logging.info("%s 클릭 성공 (selectors=%s)", description, selectors)
        else:
            logging.debug("%s 클릭 실패 (selectors=%s)", description, selectors)
        return ok
    except Exception as exc:
        logging.debug("%s 클릭 시도 중 예외: %s (selectors=%s)", description, exc, selectors)
        return False
@ensure_seconds_measured
def _handle_location_step(
    driver,
    wait: WebDriverWait,
    address_text: str,
    ha_url: str,
) -> bool:
    """Handle location step: fill address search, click icon, then Next."""
    logging.info("주소 입력 단계를 자동화합니다.")
    address_selectors = [
        "input[name='search']",
        "input[name='address']",
        "input.mdc-text-field__input[name='search']",
        "input.mdc-text-field__input[name='address']",
        "ha-textfield[label*='주소']",
        "ha-textfield[label*='검색']",
        "ha-textfield[label*='address']",
    ]
    present = any(_get_selector_counts(driver, sel)[1] > 0 for sel in address_selectors)
    if not present:
        logging.info("주소 입력 필드가 감지되지 않아 위치 단계는 건너뜁니다.")
        return True
    if not address_text:
        logging.warning("주소 검색 텍스트가 비어 있습니다.")
        return False
    filled = False
    for sel in address_selectors:
        logging.debug("주소 입력 selector 시도: %s", sel)
        if _fill_input_via_shadow(driver, sel, address_text):
            filled = True
            break
        if _fill_input_via_selector(driver, sel, address_text):
            filled = True
            break
    if not filled:
        logging.warning("주소 입력에 실패했습니다.")
        return False
    ensure_slept(milliseconds=500)
    # 검색 실행 아이콘 버튼
    icon_button_candidates = [
        "button.mdc-icon-button",
        "ha-location-picker button.mdc-icon-button",
        "ha-onboarding-map button.mdc-icon-button",
    ]
    if not _click_element_via_shadow(driver, icon_button_candidates, "주소 검색 실행 버튼"):
        logging.warning("주소 검색 실행 버튼 클릭 실패")
        return False
    ensure_slept(milliseconds=800)
    # 브라우저 권한 다이얼로그 회피를 위해 사전 권한 승인 시도
    _try_grant_geolocation_permission(driver, ha_url)
    # 위치 권한 다이얼로그가 나타날 때까지 명시적으로 대기
    dialog_resolved = True
    if _wait_until_location_permission_dialog_present(driver, max_wait_seconds=8):
        # 내부 다이얼로그 우선 처리
        ok_selectors = [
            "ha-dialog button.button.has-label",
            "ha-button > button.button.has-label",
            "button.button.has-label",
            "[role='dialog'] button.button.has-label",
            "dialog[role='alertdialog'] .actions ha-button > button.button.has-label",
            "dialog-box ha-button[autofocus] > button.button.has-label",
            "ha-md-dialog ha-button[autofocus] > button.button.has-label",
        ]
        clicked = False
        # 1차: 명시적 OK/확인 텍스트 버튼
        for t in ["OK", "확인", "허용", "Allow"]:
            if _click_by_text_deep(driver, t):
                logging.info("권한 다이얼로그 '%s' 클릭 완료", t)
                ensure_slept(milliseconds=400)
                clicked = True
                break
        # 2차: 버튼 구조 셀렉터 클릭
        if not clicked and _click_element_via_shadow(driver, ok_selectors, "권한 다이얼로그 OK 버튼"):
            ensure_slept(milliseconds=400)
            clicked = True
        # 3차: 컨테이너 기반 기본 버튼
        if not clicked and (_click_primary_button_in_dialog(driver) or _click_dialog_ok_via_structure(driver)):
            ensure_slept(milliseconds=400)
            clicked = True
        # 4차: 브라우저 alert (fallback)
        if not clicked:
            try:
                alert = driver.switch_to.alert
                text = alert.text
                logging.info("브라우저 권한 다이얼로그 감지(fallback): %s", text)
                alert.accept()
                ensure_slept(milliseconds=500)
                clicked = True
            except Exception:
                pass
        dialog_resolved = clicked
    # 다이얼로그가 감지되었으나 해소하지 못했다면 '다음'을 누르지 않음
    if not dialog_resolved:
        logging.warning("위치 권한 다이얼로그를 해소하지 못해 '다음' 클릭을 중단합니다.")
        return False
    # 다음 버튼 (텍스트 기반 1회 클릭; env 입력 유도 없이 처리) - 다이얼로그 처리 이후에만 실행
    if _click_by_text_deep(driver, "다음") or _click_by_text_deep(driver, "Next"):
        ensure_slept(milliseconds=600)
        # 다음 클릭 후에도 늦게 뜨는 권한 다이얼로그가 있을 수 있어 한 번 더 처리
        if _is_location_permission_dialog_present(driver):
            try:
                alert = driver.switch_to.alert
                text = alert.text
                logging.info("브라우저 권한 다이얼로그(지연) 감지: %s", text)
                alert.accept()
                ensure_slept(milliseconds=400)
            except Exception:
                ok_selectors = [
                    "ha-dialog button.button.has-label",
                    "ha-button > button.button.has-label",
                    "button.button.has-label",
                    "[role='dialog'] button.button.has-label",
                ]
                if _click_element_via_shadow(driver, ok_selectors, "권한 다이얼로그 OK 버튼(지연)"):
                    ensure_slept(milliseconds=300)
                else:
                    for t in ["OK", "확인", "허용", "Allow"]:
                        if _click_by_text_deep(driver, t):
                            logging.info("권한 다이얼로그(지연) '%s' 클릭 완료", t)
                            ensure_slept(milliseconds=300)
                            break
    else:
        logging.warning("다음 버튼 텍스트 기반 클릭 실패")
        return False
    return True

@ensure_seconds_measured
def _handle_login_step(
    *,
    driver,
    wait: WebDriverWait,
    user_name: str,
    password: str,
    ha_url: str,
) -> bool:
    """Handle login page: fill username/password and click Login."""
    html = driver.page_source or ""
    shallow_u, deep_u = _get_selector_counts(driver, "input[name='username'], input.mdc-text-field__input[name='username']")
    shallow_p, deep_p = _get_selector_counts(driver, "input[name='password'], input.mdc-text-field__input[name='password']")
    is_login = ("집에 오신 것을 환영합니다" in html) or (deep_u > 0 and deep_p > 0)
    if not is_login:
        logging.info("로그인 페이지로 감지되지 않아 단계를 건너뜁니다.")
        return True
    # 입력
    pairs = [
        ("사용자 이름", ["input.mdc-text-field__input[name='username']", "input[name='username']"], user_name),
        ("비밀번호", ["input.mdc-text-field__input[name='password']", "input[name='password']"], password),
    ]
    for desc, sels, val in pairs:
        ok = False
        for sel in sels:
            if _fill_input_via_shadow(driver, sel, val):
                ok = True
                break
        if not ok:
            for sel in sels:
                if _fill_input_via_selector(driver, sel, val):
                    ok = True
                    break
        if not ok:
            logging.warning("로그인 필드(%s) 입력 실패", desc)
            return False
    # 로그인 버튼
    if _click_by_text_deep(driver, "로그인"):
        ensure_slept(milliseconds=700)
        # 로그인 후 둘러보기 페이지로 이동 확인
        _ensure_overview_page_after_login(driver, wait, ha_url)
        return True
    clicked = ensure_ha_button_clicked(
        driver=driver,
        wait=wait,
        ha_url=ha_url,
        default_text="로그인",
        button_text_env_key="ha_login_button_text",
        locator_env_key="ha_login_button_locator",
        description="로그인 버튼",
    )
    if clicked:
        ensure_slept(milliseconds=700)
        # 로그인 후 둘러보기 페이지로 이동 확인
        _ensure_overview_page_after_login(driver, wait, ha_url)
        return True
    if _click_element_via_shadow(driver, ["ha-button", "button.button.has-label"], "로그인 버튼(대체)"):
        ensure_slept(milliseconds=700)
        # 로그인 후 둘러보기 페이지로 이동 확인
        _ensure_overview_page_after_login(driver, wait, ha_url)
        return True
    return False

@ensure_seconds_measured
def _ensure_overview_page_after_login(driver, wait: WebDriverWait, ha_url: str) -> bool:
    """
    로그인 후 둘러보기 페이지로 이동했는지 확인하고, 필요시 이동합니다.
    둘러보기 페이지가 확인되면 True를 반환합니다.
    """
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    
    # 로그인 후 페이지 로딩 대기 (더 긴 대기 시간)
    ensure_slept(milliseconds=3000)
    
    # 현재 URL 확인
    try:
        current_url = driver.current_url or ""
        logging.debug("로그인 후 현재 URL: %s", current_url)
    except Exception:
        current_url = ""
    
    # 현재 페이지 판별
    current_page = _detect_current_page(driver)
    logging.info("로그인 후 페이지 판별 결과: %s (URL: %s)", current_page, current_url)
    
    # 이미 둘러보기 페이지인 경우
    if current_page == "overview":
        logging.info("로그인 후 둘러보기 페이지에 있습니다.")
        return True
    
    # 온보딩 단계가 남아있는 경우는 온보딩 함수에서 처리하므로 여기서는 둘러보기로 이동하지 않음
    if current_page in ["onboarding_location", "onboarding_country", "onboarding_help", "onboarding_ready"]:
        logging.info("로그인 후 온보딩 단계가 남아있습니다. 온보딩 완료 후 둘러보기 페이지로 이동합니다.")
        return False
    
    # 인증 페이지나 로그인 페이지인 경우 - 세션이 끊어진 것일 수 있음
    # 이 경우 다시 로그인해야 할 수도 있지만, 일단 둘러보기 페이지로 이동 시도
    if current_page in ["auth", "login", "unknown"]:
        logging.warning("로그인 후 인증/로그인 페이지로 감지되었습니다. 세션이 유지되지 않았을 수 있습니다.")
        logging.info("둘러보기 페이지로 이동을 시도합니다.")
        overview_url = ha_url.rstrip("/") + "/"
        try:
            # 현재 쿠키 확인 (디버깅용)
            try:
                cookies = driver.get_cookies()
                logging.debug("현재 쿠키 개수: %d", len(cookies))
            except Exception:
                pass
            
            driver.get(overview_url)
            ensure_slept(milliseconds=3000)  # 페이지 로딩 대기
            
            # 다시 페이지 판별
            current_page_after_nav = _detect_current_page(driver)
            current_url_after_nav = driver.current_url or ""
            logging.info("둘러보기 페이지 이동 후 판별 결과: %s (URL: %s)", current_page_after_nav, current_url_after_nav)
            
            if current_page_after_nav == "overview":
                logging.info("둘러보기 페이지로 이동 완료.")
                return True
            else:
                logging.warning("둘러보기 페이지로 이동했지만 여전히 다른 페이지입니다. (판별 결과: %s, URL: %s)", current_page_after_nav, current_url_after_nav)
                return False
        except Exception as e:
            logging.error("둘러보기 페이지로 이동 중 오류: %s", e, exc_info=True)
            return False
    
    return False

@ensure_seconds_measured
def _click_by_text_deep(driver, target_text: str) -> bool:
    """Click element by visible text across shadow DOM."""
    script = """
        const target = (arguments[0] || '').trim();
        if (!target) return false;
        function normalize(s){return (s||'').replace(/\\s+/g,' ').trim();}
        function clickable(el){
            while(el && el !== document){
                if (el.matches && el.matches('button, ha-button, mwc-button')) return el;
                el = el.parentNode || el.host || el.parentElement;
            }
            return null;
        }
        function search(node){
            if(!node) return null;
            const el = clickable(node);
            if (el){
                const text = normalize(node.textContent||'');
                if (text.includes(target)) return el;
            }
            if(node.shadowRoot){
                const s = search(node.shadowRoot);
                if(s) return s;
            }
            const kids = node.children ? Array.from(node.children)
                : Array.from(node.childNodes||[]).filter(n=>n.nodeType===Node.ELEMENT_NODE);
            for(const k of kids){
                const s = search(k);
                if(s) return s;
            }
            return null;
        }
        const found = search(document.body);
        if(!found) return false;
        try{ found.click(); return true; }catch(e){ return false; }
    """
    try:
        return bool(driver.execute_script(script, target_text))
    except Exception:
        return False

@ensure_seconds_measured
def _handle_country_step(
    driver,
    wait: WebDriverWait,
    ha_url: str,
) -> bool:
    """Handle country selection: ensure '대한민국' selected; click Next."""
    logging.info("국가 설정 단계를 자동화합니다.")
    if not _is_country_page(driver):
        logging.info("국가 설정 페이지로 감지되지 않아 단계를 건너뜁니다.")
        return True
    # 현재 선택된 국가 텍스트 읽기
    read_script = """
        function getSelectedText() {
            // Try MDC structure
            const deepFind = (root, sel) => {
                function search(node){
                    if(!node) return null;
                    try{
                        if(node.matches && node.matches(sel)) return node;
                    }catch(e){}
                    if(node.shadowRoot){
                        const s = search(node.shadowRoot);
                        if(s) return s;
                    }
                    const kids = node.children ? Array.from(node.children)
                        : Array.from(node.childNodes||[]).filter(n=>n.nodeType===Node.ELEMENT_NODE);
                    for(const k of kids){
                        const s = search(k);
                        if(s) return s;
                    }
                    return null;
                }
                return search(root||document.body);
            };
            const el = deepFind(document.body, '.mdc-select__selected-text');
            if (el && el.textContent) return el.textContent.trim();
            // Try mwc-select value
            const mwc = deepFind(document.body, 'mwc-select');
            if (mwc && (mwc.value || mwc.selectedText)) {
                return (mwc.selectedText || mwc.value || '').toString().trim();
            }
            return '';
        }
        return getSelectedText();
    """
    try:
        selected = (driver.execute_script(read_script) or "").strip()
    except Exception:
        selected = ""
    logging.info("현재 선택된 국가: %s", selected or "<empty>")
    # '대한민국' 아니면 선택 시도
    should_change = not selected or ("대한민국" not in selected)
    if should_change:
        # 앵커 클릭으로 목록 열기
        anchor_selectors = [
            ".mdc-select__anchor",
            "mwc-select",
        ]
        _click_element_via_shadow(driver, anchor_selectors, "국가 선택 앵커")
        ensure_slept(milliseconds=300)
        # 목록에서 '대한민국' 항목 클릭
        if not _click_by_text_deep(driver, "대한민국"):
            # 영문 항목명 대체
            if not _click_by_text_deep(driver, "South Korea"):
                logging.warning("국가 목록에서 '대한민국'을 찾지 못했습니다.")
                # 그래도 계속 진행
        ensure_slept(milliseconds=400)
    # 다음 버튼 클릭
    if _click_by_text_deep(driver, "다음") or _click_by_text_deep(driver, "Next"):
        ensure_slept(milliseconds=500)
        return True
    # 대체 셀렉터로 시도
    if _click_element_via_shadow(driver, ["ha-button > button.button.has-label", "button.button.has-label"], "다음 버튼(국가 단계)"):
        ensure_slept(milliseconds=500)
        return True
    logging.warning("국가 설정 단계에서 다음 버튼 클릭 실패")
    return False

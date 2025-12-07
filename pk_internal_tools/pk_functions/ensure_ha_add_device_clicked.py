#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Home Assistant "Add device" 메뉴 항목을 클릭하는 함수.

둘러보기(Overview) 페이지에서 "Add to Home Assistant" 버튼을 클릭한 후
나타나는 메뉴에서 "Add device" 항목을 클릭합니다.
"""
import logging
from typing import Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pk_internal_tools.pk_functions.ensure_pk_log_cleared import ensure_pk_log_cleared
from pk_internal_tools.pk_functions.ensure_pk_log_useless_removed import ensure_pk_log_useless_removed
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)


@ensure_seconds_measured
def ensure_ha_add_device_clicked(
    driver,
    wait: WebDriverWait,
    *,
    timeout_seconds: Optional[int] = None,
) -> bool:
    """
    Home Assistant에서 "Add device" 메뉴 항목을 클릭합니다.
    
    :param driver: Selenium WebDriver
    :param wait: WebDriverWait 인스턴스
    :param timeout_seconds: 타임아웃 (초), None이면 wait의 timeout 사용
    :return: 클릭 성공 여부
    """
    timeout = timeout_seconds or wait._timeout  # noqa: SLF001
    
    logging.info("'Add device' 메뉴 항목 클릭을 시도합니다.")
    
    # Shadow DOM을 통해 "Add device" 텍스트를 가진 ha-list-item 찾기
    script = """
        const targetText = 'Add device';
        function normalize(text) {
            if (!text) return '';
            return text.replace(/\\s+/g, ' ').trim();
        }
        
        function findListItem(root, depth = 0) {
            if (!root || depth > 10) return null;
            
            // ha-list-item 요소 찾기
            if (root.tagName && root.tagName.toLowerCase() === 'ha-list-item') {
                const textContent = normalize(root.textContent || root.innerText || '');
                if (textContent.includes(targetText)) {
                    return root;
                }
            }
            
            // Shadow DOM 탐색
            if (root.shadowRoot) {
                const found = findListItem(root.shadowRoot, depth + 1);
                if (found) return found;
            }
            
            // 자식 요소 탐색
            const children = root.children ? Array.from(root.children)
                : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
            for (const child of children) {
                const found = findListItem(child, depth + 1);
                if (found) return found;
            }
            
            return null;
        }
        
        const item = findListItem(document.body);
        if (!item) return false;
        
        // 요소가 보이도록 스크롤
        item.scrollIntoView({behavior: 'smooth', block: 'center'});
        
        // 클릭 시도
        try {
            item.click();
            return true;
        } catch (e) {
            // 클릭 실패 시 이벤트로 시도
            try {
                const clickEvent = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                item.dispatchEvent(clickEvent);
                return true;
            } catch (e2) {
                console.error('Failed to click Add device:', e2);
                return false;
            }
        }
    """
    
    try:
        clicked = driver.execute_script(script)
        if clicked:
            logging.info("'Add device' 메뉴 항목 클릭 성공")
            return True
        else:
            logging.warning("'Add device' 메뉴 항목을 찾을 수 없습니다.")
            return False
    except Exception as exc:
        logging.error("'Add device' 메뉴 항목 클릭 중 오류 발생: %s", exc, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_ha_device_search_input_filled(
    driver,
    wait: WebDriverWait,
    search_text: str = "TP-Link",
    *,
    timeout_seconds: Optional[int] = None,
) -> bool:
    """
    Home Assistant 장치 추가 페이지에서 검색 입력 필드에 텍스트를 입력합니다.
    
    :param driver: Selenium WebDriver
    :param wait: WebDriverWait 인스턴스
    :param search_text: 입력할 텍스트 (기본값: "TP-Link")
    :param timeout_seconds: 타임아웃 (초), None이면 wait의 timeout 사용
    :return: 입력 성공 여부
    """
    timeout = timeout_seconds or wait._timeout  # noqa: SLF001
    
    logging.info("장치 검색 입력 필드에 '%s' 입력을 시도합니다.", search_text)
    
    # Shadow DOM을 통해 input.mdc-text-field__input 찾기
    script = """
        const searchValue = arguments[0] || '';
        if (!searchValue) return false;
        
        function findInput(root, depth = 0) {
            if (!root || depth > 10) return null;
            
            // input.mdc-text-field__input 요소 찾기
            if (root.tagName && root.tagName.toLowerCase() === 'input') {
                const classes = root.className || '';
                if (classes.includes('mdc-text-field__input')) {
                    return root;
                }
            }
            
            // Shadow DOM 탐색
            if (root.shadowRoot) {
                const found = findInput(root.shadowRoot, depth + 1);
                if (found) return found;
            }
            
            // 자식 요소 탐색
            const children = root.children ? Array.from(root.children)
                : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
            for (const child of children) {
                const found = findInput(child, depth + 1);
                if (found) return found;
            }
            
            return null;
        }
        
        const input = findInput(document.body);
        if (!input) return false;
        
        // 요소가 보이도록 스크롤
        input.scrollIntoView({behavior: 'smooth', block: 'center'});
        
        // 포커스 및 입력
        try {
            input.focus();
            input.value = '';
            input.value = searchValue;
            
            // 입력 이벤트 발생
            const inputEvent = new Event('input', { bubbles: true, cancelable: true });
            input.dispatchEvent(inputEvent);
            
            const changeEvent = new Event('change', { bubbles: true, cancelable: true });
            input.dispatchEvent(changeEvent);
            
            return true;
        } catch (e) {
            console.error('Failed to fill input:', e);
            return false;
        }
    """
    
    try:
        filled = driver.execute_script(script, search_text)
        if filled:
            logging.info("장치 검색 입력 필드에 '%s' 입력 성공", search_text)
            return True
        else:
            logging.warning("장치 검색 입력 필드를 찾을 수 없습니다.")
            return False
    except Exception as exc:
        logging.error("장치 검색 입력 필드 입력 중 오류 발생: %s", exc, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_ha_integration_item_clicked(
    driver,
    wait: WebDriverWait,
    integration_name: str,
    *,
    timeout_seconds: Optional[int] = None,
) -> bool:
    """
    Home Assistant 통합 목록에서 특정 통합 항목을 클릭합니다.
    
    :param driver: Selenium WebDriver
    :param wait: WebDriverWait 인스턴스
    :param integration_name: 클릭할 통합 이름 (예: "TP-Link", "Tapo")
    :param timeout_seconds: 타임아웃 (초), None이면 wait의 timeout 사용
    :return: 클릭 성공 여부
    """
    timeout = timeout_seconds or wait._timeout  # noqa: SLF001
    
    logging.info("'%s' 통합 항목 클릭을 시도합니다.", integration_name)
    
    # Shadow DOM을 통해 통합 이름을 가진 ha-integration-list-item 찾기
    script = """
        const targetName = arguments[0] || '';
        if (!targetName) return false;
        
        function normalize(text) {
            if (!text) return '';
            return text.replace(/\\s+/g, ' ').trim();
        }
        
        function findIntegrationItem(root, depth = 0) {
            if (!root || depth > 10) return null;
            
            // ha-integration-list-item 요소 찾기
            if (root.tagName && root.tagName.toLowerCase() === 'ha-integration-list-item') {
                const textContent = normalize(root.textContent || root.innerText || '');
                if (textContent.includes(targetName)) {
                    return root;
                }
            }
            
            // Shadow DOM 탐색
            if (root.shadowRoot) {
                const found = findIntegrationItem(root.shadowRoot, depth + 1);
                if (found) return found;
            }
            
            // 자식 요소 탐색
            const children = root.children ? Array.from(root.children)
                : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
            for (const child of children) {
                const found = findIntegrationItem(child, depth + 1);
                if (found) return found;
            }
            
            return null;
        }
        
        const item = findIntegrationItem(document.body);
        if (!item) return false;
        
        // 요소가 보이도록 스크롤
        item.scrollIntoView({behavior: 'smooth', block: 'center'});
        
        // 클릭 시도
        try {
            item.click();
            return true;
        } catch (e) {
            // 클릭 실패 시 이벤트로 시도
            try {
                const clickEvent = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                item.dispatchEvent(clickEvent);
                return true;
            } catch (e2) {
                console.error('Failed to click integration item:', e2);
                return false;
            }
        }
    """
    
    try:
        clicked = driver.execute_script(script, integration_name)
        if clicked:
            logging.info("'%s' 통합 항목 클릭 성공", integration_name)
            return True
        else:
            logging.warning("'%s' 통합 항목을 찾을 수 없습니다.", integration_name)
            return False
    except Exception as exc:
        logging.error("'%s' 통합 항목 클릭 중 오류 발생: %s", integration_name, exc, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_ha_add_to_home_assistant_button_clicked(
    driver,
    wait: WebDriverWait,
    *,
    timeout_seconds: Optional[int] = None,
) -> bool:
    """
    Home Assistant 둘러보기 페이지에서 "Add to Home Assistant" 버튼(+, mwc-icon-button)을 클릭합니다.
    
    :param driver: Selenium WebDriver
    :param wait: WebDriverWait 인스턴스
    :param timeout_seconds: 타임아웃 (초), None이면 wait의 timeout 사용
    :return: 클릭 성공 여부
    """
    timeout = timeout_seconds or wait._timeout  # noqa: SLF001

    ensure_pk_log_cleared() # pk_* : for debugging
    logging.info("'Add to Home Assistant' 버튼(+) 클릭을 시도합니다.")
    
    # 먼저 둘러보기 페이지인지 확인
    from pk_internal_tools.pk_functions.ensure_home_assistant_onboarding_completed import _is_overview_page, _detect_current_page
    current_url = driver.current_url
    detected_page = _detect_current_page(driver)
    logging.info("현재 페이지 판별: %s (URL: %s)", detected_page, current_url)
    
    # 둘러보기 페이지가 아니면 처리
    if detected_page != "overview":
        # 인증 페이지인 경우 로그인을 다시 수행
        if detected_page == "auth":
            logging.warning("인증 페이지로 리다이렉트되었습니다. 로그인을 다시 수행합니다.")
            from pk_internal_tools.pk_functions.ensure_home_assistant_onboarding_completed import _handle_login_step
            from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
            from urllib.parse import urlparse
            parsed = urlparse(current_url)
            ha_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # 로그인 정보 가져오기
            ha_user_name_for_login = ensure_env_var_completed_2025_11_24(
                key_name="HA_ONBOARDING_USERNAME",
                func_n="ensure_ha_add_to_home_assistant_button_clicked",
                guide_text="Home Assistant 사용자 이름을 입력하세요:",
            )
            ha_password_for_login = ensure_env_var_completed_2025_11_24(
                key_name="HA_ONBOARDING_PASSWORD",
                func_n="ensure_ha_add_to_home_assistant_button_clicked",
                guide_text="Home Assistant 비밀번호를 입력하세요:",
            )
            
            # 로그인 페이지로 이동 (인증 페이지에서 로그인 페이지로 이동)
            login_url = ha_url + "/auth/login"
            logging.info("로그인 페이지로 이동: %s", login_url)
            driver.get(login_url)
            from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
            ensure_slept(milliseconds=3000)
            
            # 로그인 수행
            if _handle_login_step(
                driver=driver,
                wait=wait,
                user_name=ha_user_name_for_login,
                password=ha_password_for_login,
                ha_url=ha_url,
            ):
                logging.info("로그인 완료. 둘러보기 페이지로 이동합니다.")
                ensure_slept(milliseconds=2000)
                # 다시 페이지 판별
                detected_page = _detect_current_page(driver)
                logging.info("로그인 후 페이지 판별: %s", detected_page)
            else:
                logging.error("로그인 실패. 계속 진행합니다.")
        else:
            logging.warning("둘러보기 페이지가 아닙니다 (%s). 둘러보기 페이지로 이동합니다.", detected_page)
            # URL에서 기본 경로 추출
            if "/auth" in current_url:
                base_url = current_url.split("/auth")[0] + "/"
            elif "/lovelace" in current_url:
                base_url = current_url.split("/lovelace")[0] + "/"
            else:
                # URL에서 포트까지 추출 (예: http://119.207.161.56:8123/)
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}/"
            
            logging.info("둘러보기 페이지로 이동: %s", base_url)
            driver.get(base_url)
            # 페이지 로딩 대기
            from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
            ensure_slept(milliseconds=3000)
            
            # 다시 페이지 판별
            detected_page = _detect_current_page(driver)
            logging.info("이동 후 페이지 판별: %s", detected_page)
            
            if detected_page != "overview":
                logging.warning("둘러보기 페이지로 이동했지만 여전히 둘러보기 페이지가 아닙니다. 계속 진행합니다.")
    
    # 여러 방법으로 버튼 찾기 시도
    # 1. aria-label로 찾기 (button 또는 mwc-icon-button 내부의 button)
    # 2. mwc-icon-button으로 찾기
    # 3. button.mdc-icon-button으로 찾기
    script = """
        const targetAriaLabel = 'Add to Home Assistant';
        
        function findButton(root, depth = 0) {
            if (!root || depth > 15) return null;  // depth 증가
            
            // button 요소 찾기 (button.mdc-icon-button)
            if (root.tagName) {
                const tagName = root.tagName.toLowerCase();
                if (tagName === 'button') {
                    const ariaLabel = root.getAttribute('aria-label') || '';
                    const classes = root.className || '';
                    // button.mdc-icon-button이고 aria-label이 "Add to Home Assistant"를 포함하는지 확인
                    if (classes.includes('mdc-icon-button')) {
                        // aria-label이 정확히 일치하거나 포함되는지 확인 (끝 공백 무시)
                        const normalizedLabel = ariaLabel.trim();
                        if (normalizedLabel.includes(targetAriaLabel) || 
                            normalizedLabel === 'Add to Home Assistant' ||
                            normalizedLabel === 'Add to Home Assistant ') {
                            console.log('Found button by aria-label:', normalizedLabel);
                            return root;
                        }
                    }
                }
                // mwc-icon-button 요소도 확인 (Shadow DOM 내부에 있을 수 있음)
                if (tagName === 'mwc-icon-button') {
                    const ariaLabel = root.getAttribute('aria-label') || '';
                    const normalizedLabel = ariaLabel.trim();
                    if (normalizedLabel.includes(targetAriaLabel) || 
                        normalizedLabel === 'Add to Home Assistant' ||
                        normalizedLabel === 'Add to Home Assistant ') {
                        console.log('Found mwc-icon-button by aria-label:', normalizedLabel);
                        // mwc-icon-button 내부의 button 찾기
                        if (root.shadowRoot) {
                            const innerButton = root.shadowRoot.querySelector('button');
                            if (innerButton) return innerButton;
                        }
                        return root;
                    }
                }
            }
            
            // Shadow DOM 탐색 (더 깊이 탐색)
            if (root.shadowRoot) {
                const found = findButton(root.shadowRoot, depth + 1);
                if (found) return found;
            }
            
            // 자식 요소 탐색
            const children = root.children ? Array.from(root.children)
                : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
            for (const child of children) {
                const found = findButton(child, depth + 1);
                if (found) return found;
            }
            
            return null;
        }
        
        // 먼저 aria-label로 찾기
        let button = findButton(document.body);
        
        // 찾지 못하면 button.mdc-icon-button으로 찾기
        if (!button) {
            function findAllIconButtons(root, depth = 0) {
                if (!root || depth > 10) return [];
                const results = [];
                
                if (root.tagName && root.tagName.toLowerCase() === 'button') {
                    const classes = root.className || '';
                    if (classes.includes('mdc-icon-button')) {
                        results.push(root);
                    }
                }
                
                if (root.shadowRoot) {
                    results.push(...findAllIconButtons(root.shadowRoot, depth + 1));
                }
                
                const children = root.children ? Array.from(root.children)
                    : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
                for (const child of children) {
                    results.push(...findAllIconButtons(child, depth + 1));
                }
                
                return results;
            }
            
            const allButtons = findAllIconButtons(document.body);
            // aria-label이 "Add to Home Assistant"인 button 찾기
            for (const btn of allButtons) {
                const ariaLabel = btn.getAttribute('aria-label') || '';
                if (ariaLabel.trim().includes(targetAriaLabel)) {
                    button = btn;
                    console.log('Found button.mdc-icon-button by aria-label');
                    break;
                }
            }
            // 여전히 못 찾으면 첫 번째 button.mdc-icon-button 시도
            if (!button && allButtons.length > 0) {
                button = allButtons[0];
                console.log('Found button.mdc-icon-button by position');
            }
        }
        
        if (!button) {
            console.error('Add to Home Assistant button not found');
            return false;
        }
        
        // 요소가 보이도록 스크롤
        button.scrollIntoView({behavior: 'smooth', block: 'center'});
        
        // 요소가 클릭 가능한지 확인
        const rect = button.getBoundingClientRect();
        const isVisible = rect.width > 0 && rect.height > 0 && 
                         window.getComputedStyle(button).display !== 'none' &&
                         window.getComputedStyle(button).visibility !== 'hidden';
        
        if (!isVisible) {
            console.error('Button is not visible');
            return false;
        }
        
        // 클릭 시도
        try {
            button.focus();
            button.click();
            return true;
        } catch (e) {
            // 클릭 실패 시 이벤트로 시도
            try {
                const clickEvent = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window,
                    button: 0
                });
                button.dispatchEvent(clickEvent);
                return true;
            } catch (e2) {
                // 마지막으로 mousedown/mouseup 이벤트 시도
                try {
                    button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                    button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                    button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                    return true;
                } catch (e3) {
                    console.error('Failed to click Add to Home Assistant:', e3);
                    return false;
                }
            }
        }
    """
    
    try:
        # 페이지가 완전히 로드될 때까지 대기
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        
        # 1. 페이지 로딩 완료 대기
        def wait_for_page_load(driver, max_wait=15):
            """페이지가 완전히 로드될 때까지 대기"""
            import time
            start_time = time.time()
            while time.time() - start_time < max_wait:
                ready_state = driver.execute_script("return document.readyState")
                if ready_state == "complete":
                    # 추가로 긴 대기 (동적 콘텐츠 로딩, 특히 Shadow DOM)
                    ensure_slept(milliseconds=2000)
                    return True
                ensure_slept(milliseconds=200)
            return False
        
        wait_for_page_load(driver, max_wait=15)
        
        # 2. 버튼이 나타날 때까지 재시도 (최대 5초)
        max_retries = 10
        retry_delay = 500  # milliseconds
        
        clicked = False
        for attempt in range(max_retries):
            # 디버깅: 현재 페이지에서 버튼 요소 찾기 시도
            debug_script = """
            function findAllButtons(root, depth = 0) {
                if (!root || depth > 10) return [];
                const results = [];
                
                if (root.tagName && root.tagName.toLowerCase() === 'button') {
                    const classes = root.className || '';
                    const ariaLabel = root.getAttribute('aria-label') || '';
                    if (classes.includes('mdc-icon-button')) {
                        results.push({
                            tag: 'button',
                            classes: classes,
                            ariaLabel: ariaLabel,
                            visible: root.offsetWidth > 0 && root.offsetHeight > 0
                        });
                    }
                }
                
                // mwc-icon-button도 찾기
                if (root.tagName && root.tagName.toLowerCase() === 'mwc-icon-button') {
                    const ariaLabel = root.getAttribute('aria-label') || '';
                    results.push({
                        tag: 'mwc-icon-button',
                        ariaLabel: ariaLabel,
                        visible: root.offsetWidth > 0 && root.offsetHeight > 0
                    });
                }
                
                if (root.shadowRoot) {
                    results.push(...findAllButtons(root.shadowRoot, depth + 1));
                }
                
                const children = root.children ? Array.from(root.children)
                    : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
                for (const child of children) {
                    results.push(...findAllButtons(child, depth + 1));
                }
                
                return results;
            }
            return findAllButtons(document.body);
            """
            
            try:
                found_buttons = driver.execute_script(debug_script)
                if found_buttons:
                    logging.info("시도 %d/%d: 발견된 button.mdc-icon-button 요소들: %s", attempt + 1, max_retries, found_buttons)
                else:
                    logging.warning("시도 %d/%d: button.mdc-icon-button 요소를 찾지 못했습니다.", attempt + 1, max_retries)
                    
                # 추가 디버깅: 페이지의 모든 버튼 요소 확인
                all_buttons_script = """
                function findAllButtons(root, depth = 0) {
                    if (!root || depth > 5) return [];
                    const results = [];
                    
                    if (root.tagName && root.tagName.toLowerCase() === 'button') {
                        const ariaLabel = root.getAttribute('aria-label') || '';
                        const classes = root.className || '';
                        results.push({
                            tag: 'button',
                            classes: classes.substring(0, 50),  // 길이 제한
                            ariaLabel: ariaLabel.substring(0, 50),
                            visible: root.offsetWidth > 0 && root.offsetHeight > 0
                        });
                    }
                    
                    if (root.shadowRoot) {
                        results.push(...findAllButtons(root.shadowRoot, depth + 1));
                    }
                    
                    const children = root.children ? Array.from(root.children)
                        : Array.from(root.childNodes || []).filter(n => n.nodeType === Node.ELEMENT_NODE);
                    for (const child of children) {
                        results.push(...findAllButtons(child, depth + 1));
                    }
                    
                    return results;
                }
                return findAllButtons(document.body).slice(0, 20);  // 최대 20개만
                """
                try:
                    all_buttons = driver.execute_script(all_buttons_script)
                    if all_buttons:
                        logging.info("페이지의 모든 button 요소 (최대 20개): %s", all_buttons)
                except Exception:
                    pass
            except Exception as debug_exc:
                logging.warning("디버깅 스크립트 실행 실패: %s", debug_exc)
            
            # 버튼 클릭 시도
            clicked = driver.execute_script(script)
            if clicked:
                break
            
            # 재시도 전 대기
            if attempt < max_retries - 1:
                logging.debug("버튼을 찾지 못했습니다. %dms 후 재시도... (시도 %d/%d)", retry_delay, attempt + 1, max_retries)
                ensure_slept(milliseconds=retry_delay)
        if clicked:
            logging.info("'Add to Home Assistant' 버튼(+) 클릭 성공")
            ensure_slept(milliseconds=500)  # 클릭 후 대기
            return True
        else:
            logging.warning("'Add to Home Assistant' 버튼(+)을 찾을 수 없습니다. DOM 상태를 확인합니다.")
            
            # 더 자세한 디버깅 정보
            try:
                # 현재 URL 확인
                current_url = driver.current_url
                logging.debug("현재 URL: %s", current_url)
                
                # 인증 페이지나 lovelace/0 페이지인 경우 실제 둘러보기 페이지(/)로 이동 후 재시도
                if "/auth" in current_url or "/lovelace/0" in current_url:
                    if "/auth" in current_url:
                        logging.info("인증 페이지에서 버튼을 찾지 못했습니다. 실제 둘러보기 페이지(/)로 이동 후 재시도합니다.")
                    else:
                        logging.info("lovelace/0 페이지에서 버튼을 찾지 못했습니다. 실제 둘러보기 페이지(/)로 이동 후 재시도합니다.")
                    
                    # URL에서 기본 경로 추출 (예: http://119.207.161.56:8123/)
                    if "/auth" in current_url:
                        # /auth/authorize?... 형태에서 기본 URL 추출
                        base_url = current_url.split("/auth")[0] + "/"
                    else:
                        base_url = current_url.split("/lovelace")[0] + "/"
                    
                    logging.info("둘러보기 페이지로 이동: %s", base_url)
                    driver.get(base_url)
                    wait_for_page_load(driver, max_wait=10)
                    ensure_slept(milliseconds=2000)
                    
                    # 재시도
                    clicked = driver.execute_script(script)
                    if clicked:
                        logging.info("'Add to Home Assistant' 버튼(+) 클릭 성공 (둘러보기 페이지로 이동 후)")
                        ensure_slept(milliseconds=500)
                        return True
                    else:
                        logging.warning("둘러보기 페이지로 이동 후에도 버튼을 찾지 못했습니다.")
                
                # 페이지 제목 확인
                page_title = driver.title
                logging.debug("페이지 제목: %s", page_title)
                
                # 간단한 CSS selector로도 시도
                from selenium.webdriver.common.by import By
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, "button.mdc-icon-button")
                    logging.debug("CSS selector로 찾은 button.mdc-icon-button 개수: %d", len(buttons))
                    for i, btn in enumerate(buttons):
                        try:
                            aria_label = btn.get_attribute('aria-label')
                            logging.debug("  버튼 %d: aria-label='%s'", i, aria_label)
                        except Exception:
                            pass
                except Exception as css_exc:
                    logging.debug("CSS selector 시도 실패: %s", css_exc)
                    
            except Exception as debug_exc:
                logging.debug("디버깅 정보 수집 실패: %s", debug_exc)
            
            return False
    except Exception as exc:
        logging.error("'Add to Home Assistant' 버튼(+) 클릭 중 오류 발생: %s", exc, exc_info=True)
        return False


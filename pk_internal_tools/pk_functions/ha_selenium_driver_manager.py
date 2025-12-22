#!/usr/bin/env python3

"""
Home Assistant Selenium WebDriver 전역 관리 모듈.

온보딩과 장치 추가 단계에서 동일한 브라우저 세션을 재사용하기 위해
드라이버를 전역 변수로 관리합니다.
"""
import logging
from typing import Optional

from seleniumbase import Driver

logger = logging.getLogger(__name__)

# 전역 드라이버 인스턴스
_ha_driver: Optional[Driver] = None


def get_ha_selenium_driver(headless_mode: bool = False) -> Driver:
    """
    Home Assistant용 Selenium WebDriver를 반환합니다.
    기존 드라이버가 있고 세션이 유효하면 재사용하고, 그렇지 않으면 새로 생성합니다.
    
    :param headless_mode: 헤드리스 모드 여부
    :return: Selenium WebDriver 인스턴스
    """
    global _ha_driver
    
    # 기존 드라이버가 있고 세션이 유효한지 확인
    if _ha_driver is not None:
        if _is_driver_session_valid(_ha_driver):
            logger.debug("기존 HA Selenium 드라이버를 재사용합니다.")
            return _ha_driver
        else:
            logger.warning("기존 HA Selenium 드라이버 세션이 유효하지 않습니다. 새로 생성합니다.")
            try:
                _ha_driver.quit()
            except Exception as e:
                logger.debug("기존 드라이버 종료 중 오류 (무시): %s", e)
            _ha_driver = None
    
    # 새 드라이버 생성
    logger.info("새 HA Selenium 드라이버를 생성합니다. (headless_mode=%s)", headless_mode)
    from pk_internal_tools.pk_functions.get_selenium_driver_initialized_for_cloudflare import (
        get_selenium_driver_initialized_for_cloudflare,
    )
    
    _ha_driver = get_selenium_driver_initialized_for_cloudflare(headless_mode=headless_mode)
    logger.info("HA Selenium 드라이버 생성 완료.")
    return _ha_driver


def _is_driver_session_valid(driver: Driver) -> bool:
    """
    드라이버 세션이 유효한지 확인합니다.
    
    :param driver: 확인할 드라이버 인스턴스
    :return: 세션이 유효하면 True, 그렇지 않으면 False
    """
    if driver is None:
        return False
    
    try:
        # session_id 확인
        session_id = driver.session_id
        if not session_id:
            return False
        
        # 간단한 명령 실행으로 세션 유효성 확인
        _ = driver.current_url
        return True
    except Exception as e:
        logger.debug("드라이버 세션 유효성 확인 실패: %s", e)
        return False


def close_ha_selenium_driver() -> None:
    """
    전역 HA Selenium 드라이버를 닫습니다.
    """
    global _ha_driver
    
    if _ha_driver is not None:
        try:
            logger.info("HA Selenium 드라이버를 종료합니다.")
            _ha_driver.quit()
        except Exception as e:
            logger.debug("드라이버 종료 중 오류 (무시): %s", e)
        finally:
            _ha_driver = None


def reset_ha_selenium_driver() -> None:
    """
    전역 HA Selenium 드라이버를 초기화합니다 (닫고 None으로 설정).
    close_ha_selenium_driver()와 동일하지만 명시적으로 리셋 의도를 표현합니다.
    """
    close_ha_selenium_driver()


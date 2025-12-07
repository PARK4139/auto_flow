#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Home Assistant Long-Lived Access Token을 얻는 함수.

사용자가 HA 웹 UI에서 토큰을 생성할 수 있도록 안내하거나,
자동으로 토큰을 생성하는 방법을 제공합니다.
"""
import logging
import webbrowser
from typing import Optional

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)

logger = logging.getLogger(__name__)


@ensure_seconds_measured
def ensure_ha_token_obtained(
    ha_url: str,
    *,
    open_browser: bool = True,
) -> Optional[str]:
    """
    Home Assistant Long-Lived Access Token을 얻습니다.
    
    :param ha_url: Home Assistant 기본 URL (예: http://localhost:8123)
    :param open_browser: 브라우저를 자동으로 열지 여부
    :return: 토큰 문자열 또는 None (사용자가 취소한 경우)
    """
    logger.info("Home Assistant Long-Lived Access Token 생성 안내")
    
    # 토큰 생성 페이지 URL
    token_url = ha_url.rstrip("/") + "/profile"
    
    print("\n" + "="*70)
    print("Home Assistant Long-Lived Access Token 생성 방법")
    print("="*70)
    print("\n1. 다음 URL로 이동하세요:")
    print(f"   {token_url}")
    print("\n2. 프로필 페이지에서 'Long-Lived Access Tokens' 섹션을 찾으세요.")
    print("   (페이지를 아래로 스크롤하면 찾을 수 있습니다)")
    print("\n3. 'Long-Lived Access Tokens' 섹션이 보이지 않으면:")
    print("   - 왼쪽 하단 프로필 아이콘 클릭")
    print("   - 또는 Settings > People & Zones > 사용자 이름 클릭")
    print("   - 또는 직접 URL: " + token_url + "#long-lived-access-tokens")
    print("\n4. 'CREATE TOKEN' 버튼을 클릭하세요.")
    print("\n5. 토큰 이름을 입력하세요 (예: 'P110M Control Token').")
    print("\n6. 'OK' 또는 '생성' 버튼을 클릭하면 토큰이 생성됩니다.")
    print("\n7. 생성된 토큰을 복사하세요 (한 번만 표시되므로 주의하세요!).")
    print("\n8. 아래에 토큰을 붙여넣으세요.")
    print("="*70 + "\n")
    
    if open_browser:
        try:
            webbrowser.open(token_url)
            logger.info("브라우저에서 토큰 생성 페이지를 열었습니다.")
        except Exception as e:
            logger.warning("브라우저를 열 수 없습니다: %s", e)
            logger.info("수동으로 다음 URL을 열어주세요: %s", token_url)
    
    # 토큰 입력 받기
    ha_token = ensure_env_var_completed(
        key_name="ha_token",
        func_n=func_n,
        guide_text="Home Assistant TOKEN을 입력",
    )
    if not ha_token:
        logger.warning("토큰이 입력되지 않았습니다.")
        return None
    return ha_token


@ensure_seconds_measured
def ensure_ha_token_obtained_via_fzf(
    ha_url: Optional[str] = None,
) -> Optional[str]:
    """
    fzf를 사용하여 HA URL을 선택한 후 토큰을 얻습니다.
    HA_IP를 우선적으로 사용합니다.
    
    :param ha_url: Home Assistant 기본 URL (None인 경우 fzf로 선택, HA_IP 우선)
    :return: 토큰 문자열 또는 None
    """
    from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_ha_api import (
        _select_ha_url_via_fzf,
    )
    
    if not ha_url:
        ha_url = _select_ha_url_via_fzf()
        if not ha_url:
            # HA IP 기반으로 기본값 설정
            try:
                from pk_internal_tools.pk_functions.ensure_env_var_completed import (
                    ensure_env_var_completed,
                )
                from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
                
                func_n = get_caller_name()
                ha_ip = ensure_env_var_completed(
                    key_name="HA_IP",
                    func_n=func_n,
                    guide_text="Home Assistant IP 주소를 입력하세요 (예: 119.207.161.56):",
                )
                if ha_ip:
                    ha_url = f"http://{ha_ip}:8123"
                else:
                    logger.error("HA URL이 선택되지 않았습니다.")
                    return None
            except Exception as e:
                logger.error("HA URL을 가져오는 중 오류 발생: %s", e)
                return None
    
    return ensure_ha_token_obtained(ha_url, open_browser=True)


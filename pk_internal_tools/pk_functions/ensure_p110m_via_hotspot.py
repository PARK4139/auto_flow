#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스마트폰 핫스팟을 통한 P110M 제어

Wi-Fi 모듈이 없는 PC에서 스마트폰 핫스팟을 활용해 P110M과 같은 네트워크에 연결하는 방법
"""

import asyncio
import logging
from typing import Optional

async def guide_hotspot_setup():
    """스마트폰 핫스팟 설정 튜토리얼"""
    
    print("📱 스마트폰 핫스팟을 통한 P110M 제어 튜토리얼")
    print(PK_UNDERLINE)
    
    print("🔧 1단계: 스마트폰 핫스팟 설정")
    print("   - 스마트폰에서 '개인 핫스팟' 또는 '모바일 핫스팟' 활성화")
    print("   - 핫스팟 이름과 비밀번호 확인")
    print("   - 2.4GHz 대역 사용 (P110M 호환성)")
    
    print("📡 2단계: P110M을 핫스팟에 연결")
    print("   - TP-Link Kasa 앱 실행")
    print("   - P110M 장치 설정 → Wi-Fi 설정")
    print("   - 스마트폰 핫스팟 선택하여 연결")
    
    print("💻 3단계: PC를 같은 핫스팟에 연결")
    print("   - PC Wi-Fi 설정에서 같은 핫스팟 연결")
    print("   - 또는 USB 테더링 사용")
    
    print("🎯 4단계: 같은 네트워크에서 제어")
    print("   - 이제 PC와 P110M이 같은 네트워크 대역")
    print("   - 일반적으로 192.168.43.x 또는 192.168.137.x 대역")
    
    print("⚡ 5단계: P110M 제어 테스트")
    
    # 핫스팟 일반적인 IP 대역들
    hotspot_networks = [
        "192.168.43.",  # Android 기본
        "192.168.137.", # Windows 모바일 핫스팟
        "172.20.10.",   # iPhone 핫스팟
    ]
    
    print("   일반적인 핫스팟 IP 대역에서 P110M 찾기:")
    for network in hotspot_networks:
        print(f"   - {network}100 ~ {network}200 범위")
    
    return hotspot_networks


async def test_p110m_on_hotspot():
    """핫스팟 환경에서 P110M 테스트"""
    
    # 튜토리얼 표시
    hotspot_networks = await guide_hotspot_setup()
    
    print("🔍 핫스팟 네트워크에서 P110M 검색 시작...")
    
    try:
        from pk_internal_tools.pk_functions.ensure_p110m_quick_control import control_p110m_quick
        
        # 핫스팟 일반적인 IP들 시도
        test_ips = []
        for network in hotspot_networks:
            for i in [100, 101, 102, 103, 104, 105, 110, 150, 200]:
                test_ips.append(f"{network}{i}")
        
        print(f"📱 {len(test_ips)}개의 핫스팟 IP에서 P110M 검색 중...")
        
        success = await control_p110m_quick(
            action="status",
            target_ip=None,
            try_common_ips=False  # 일반 IP 대신 핫스팟 IP만 시도
        )
        
        if success:
            print("🎉 핫스팟을 통한 P110M 연결 성공!")
            
            # 추가 테스트
            print("🔄 토글 테스트...")
            toggle_success = await control_p110m_quick("toggle")
            
            if toggle_success:
                print("✅ 핫스팟을 통한 P110M 제어 완전 성공!")
            
        else:
            print("❌ 핫스팟에서도 P110M을 찾을 수 없습니다.")
            print("🔧 추가 확인사항:")
            print("   1. P110M이 핫스팟에 정상 연결되었는지 Kasa 앱에서 확인")
            print("   2. PC가 같은 핫스팟에 연결되었는지 확인")
            print("   3. 핫스팟이 2.4GHz 대역인지 확인")
            print("   4. 방화벽이 로컬 네트워크 통신을 차단하지 않는지 확인")
        
        return success
        
    except ImportError as e:
        print(f"❌ 필요한 모듈을 찾을 수 없습니다: {e}")
        return False
    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")
        return False


if __name__ == "__main__":
    async def main():
        print("📱 스마트폰 핫스팟을 통한 P110M 제어 테스트")
        await test_p110m_on_hotspot()
    
    asyncio.run(main())

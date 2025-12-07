#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P110M Matter 연결 테스트 및 디버깅 도구
"""

import asyncio
import logging
from pathlib import Path

def test_p110m_connection_status():
    """P110M Matter 연결 상태를 테스트하고 디버깅 정보를 출력합니다"""
    
    print("=== P110M Matter 연결 테스트 시작")
    
    # n. 기본 설정 정보 출력
    try:
        from pk_internal_tools.pk_functions.ensure_matter_smart_plug_on import (
            WS_URL, COMMISSION_CODE, DEVICE_MAC, FINAL_TOGGLE,
            INSTALL_TIMEOUT_SEC, SERVER_READY_TIMEOUT_SEC
        )
        
        print(f"설정 정보:")
        print(f"  - WebSocket URL: {WS_URL}")
        print(f"  - Commission Code: {COMMISSION_CODE}")
        print(f"  - Device MAC: {DEVICE_MAC}")
        print(f"  - Final Toggle: {FINAL_TOGGLE}")
        print(f"  - Install Timeout: {INSTALL_TIMEOUT_SEC}s")
        print(f"  - Server Ready Timeout: {SERVER_READY_TIMEOUT_SEC}s")
        
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        return False
    
    # n. Matter Server 상태 확인
    try:
        from pk_internal_tools.pk_functions.ensure_matter_smart_plug_on import is_matter_server_running
        
        server_running = is_matter_server_running()
        print(f"Matter Server 실행 상태: {'✅ 실행 중' if server_running else '❌ 중지됨'}")
        
        if not server_running:
            print("  → Matter Server가 실행되지 않았습니다. 자동으로 시작을 시도합니다.")
            
    except Exception as e:
        print(f"❌ Matter Server 상태 확인 실패: {e}")
        return False
    
    # n. Python 환경 확인
    try:
        import sys
        print(f"Python 환경:")
        print(f"  - 버전: {sys.version.split()[0]}")
        print(f"  - 실행 경로: {sys.executable}")
        
        # CHIP 바인딩 확인
        try:
            import chip
            print(f"  - CHIP 바인딩: ✅ 사용 가능 (버전: {getattr(chip, '__version__', 'unknown')})")
        except ImportError:
            print(f"  - CHIP 바인딩: ❌ 사용 불가 (설치 필요)")
            
    except Exception as e:
        print(f"❌ Python 환경 확인 실패: {e}")
    
    # n. 네트워크 환경 확인  
    try:
        from pk_internal_tools.pk_functions.ensure_matter_smart_plug_on import (
            detect_windows_wifi_ssid_and_password, detect_windows_bluetooth_present
        )
        
        wifi_ssid, wifi_psk = detect_windows_wifi_ssid_and_password()
        ble_present = detect_windows_bluetooth_present()
        
        print(f"네트워크 환경:")
        print(f"  - Wi-Fi SSID: {wifi_ssid if wifi_ssid else '감지되지 않음'}")
        print(f"  - Wi-Fi 비밀번호: {'✅ 사용 가능' if wifi_psk else '❌ 사용 불가'}")
        print(f"  - Bluetooth: {'✅ 사용 가능' if ble_present else '❌ 사용 불가'}")
        
    except Exception as e:
        print(f"❌ 네트워크 환경 확인 실패: {e}")
    
    print("=== P110M Matter 연결 테스트 완료")
    return True

async def test_p110m_full_connection():
    """전체 P110M Matter 연결을 테스트합니다"""
    
    print("=== P110M Matter 전체 연결 테스트 시작")
    
    try:
        from pk_internal_tools.pk_functions.ensure_matter_smart_plug_on import ensure_matter_smart_plug_on
        
        # 전체 연결 프로세스 실행
        await ensure_matter_smart_plug_on()
        
        print("✅ P110M Matter 연결 테스트 성공!")
        
    except Exception as e:
        print(f"❌ P110M Matter 연결 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    print("=== P110M Matter 전체 연결 테스트 완료")
    return True

def main():
    """메인 테스트 함수"""
    print("🔌 P110M IOT 장치 Matter 연결 디버깅 도구")
    print(PK_UNDERLINE)
    
    # n. 기본 연결 상태 테스트
    if not test_p110m_connection_status():
        print("❌ 기본 테스트 실패 - 전체 테스트를 건너뜁니다.")
        return
    
    print()
    
    # n. 사용자 선택
    try:
        choice = input("전체 연결 테스트를 실행하시겠습니까? (y/N): ").strip().lower()
        if choice in ('y', 'yes'):
            asyncio.run(test_p110m_full_connection())
        else:
            print("전체 테스트를 건너뜁니다.")
    except KeyboardInterrupt:
        print("⚠️ 사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()

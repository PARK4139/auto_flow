#!/usr/bin/env python3

"""
Matter 커미셔닝 모듈
P110M 장치를 Matter 네트워크에 커미셔닝합니다.
"""

import asyncio
import logging
import subprocess
import json
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


class MatterCommissioningController:
    """Matter 커미셔닝 제어 클래스"""
    
    def __init__(self):
        self.commissioning_timeout = 300  # 5분
        self.retry_attempts = 3
        self.retry_delay = 10  # 10초
    
    async def check_p110m_led_status(self) -> str:
        """P110M LED 상태 확인 (사용자 안내)"""
        logging.debug("🔍 P110M LED 상태를 확인하세요:")
        logging.debug("   - 주황+초록 점멸: 커미셔닝 모드 (정상)")
        logging.debug("   - 초록 점등: 이미 커미셔닝됨")
        logging.debug("   - 빨간색: 오류 상태")
        logging.debug("   - 꺼짐: 전원 문제")
        
        return "checking"
    
    async def wait_for_commissioning_mode(self) -> bool:
        """커미셔닝 모드 대기"""
        logging.debug("⏳ P110M이 커미셔닝 모드로 진입할 때까지 대기 중...")
        logging.debug("💡 P110M의 전원 버튼을 5초간 길게 눌러 커미셔닝 모드를 활성화하세요")
        
        # 사용자에게 시간을 주기 위해 대기
        await asyncio.sleep(5)
        return True
    
    async def start_commissioning_process(self, commission_code: str) -> bool:
        """커미셔닝 프로세스 시작"""
        try:
            logging.debug("🚀 P110M 커미셔닝 프로세스 시작")
            logging.debug(f"📋 커미션 코드: {self._mask_commission_code(commission_code)}")
            
            # n. LED 상태 확인
            await self.check_p110m_led_status()
            
            # n. 커미셔닝 모드 대기
            if not await self.wait_for_commissioning_mode():
                return False
            
            # n. Docker 기반 커미셔닝 시도
            success = await self._commission_via_docker(commission_code)
            if success:
                return True
            
            # n. 수동 커미셔닝 안내
            await self._provide_manual_commissioning_guide(commission_code)
            return False
            
        except Exception as e:
            logging.debug(f"커미셔닝 프로세스 중 오류: {e}")
            return False
    
    async def _commission_via_docker(self, commission_code: str) -> bool:
        """Docker를 통한 자동 커미셔닝"""
        try:
            logging.debug("🐳 Docker 기반 자동 커미셔닝 시도")
            
            # Docker 명령어 구성
            docker_cmd = [
                "docker", "run", "--rm",
                "--network", "host",
                "matter/matter-controller",
                "commission",
                "--commission-code", commission_code,
                "--timeout", str(self.commissioning_timeout)
            ]
            
            cmd_str = " ".join(docker_cmd)
            logging.debug(f"Docker 커미셔닝 명령어: {cmd_str}")
            
            result = await asyncio.to_thread(ensure_command_executed, cmd_str)
            
            if result and "commissioning successful" in str(result).lower():
                logging.debug("✅ Docker 기반 커미셔닝 성공")
                return True
            else:
                logging.debug("❌ Docker 기반 커미셔닝 실패")
                return False
                
        except Exception as e:
            logging.debug(f"Docker 커미셔닝 오류: {e}")
            return False
    
    async def _provide_manual_commissioning_guide(self, commission_code: str) -> None:
        """수동 커미셔닝 튜토리얼 제공"""
        logging.debug("📱 수동 커미셔닝 튜토리얼:")
        logging.debug("   1. TP-Link Tapo 앱을 다운로드하고 설치하세요")
        logging.debug("   2. 앱에서 '장치 추가' 또는 '+' 버튼을 누르세요")
        logging.debug("   3. '스마트 플러그' 또는 'P110M'을 선택하세요")
        logging.debug("   4. Wi-Fi 네트워크를 선택하고 비밀번호를 입력하세요")
        logging.debug(f"5. 커미션 코드를 입력하세요: {self._mask_commission_code(commission_code)}")
        logging.debug("   6. P110M의 전원 버튼을 5초간 길게 눌러 커미셔닝 모드를 활성화하세요")
        logging.debug("   7. 앱의 지시에 따라 설정을 완료하세요")
        logging.debug("")
        logging.debug("💡 커미셔닝이 완료되면 P110M의 LED가 초록색으로 점등됩니다")
        logging.debug("🔄 커미셔닝 완료 후 다시 자동 제어를 시도해보세요")
    
    def _mask_commission_code(self, commission_code: str) -> str:
        """커미션 코드 마스킹"""
        if len(commission_code) <= 8:
            return "*" * len(commission_code)
        else:
            return commission_code[:4] + "*" * (len(commission_code) - 8) + commission_code[-4:]
    
    async def verify_commissioning(self, commission_code: str) -> bool:
        """커미셔닝 검증"""
        try:
            logging.debug("🔍 커미셔닝 상태 검증 중...")
            
            # Docker를 통한 상태 확인
            docker_cmd = [
                "docker", "run", "--rm",
                "--network", "host",
                "matter/matter-controller",
                "status",
                "--commission-code", commission_code
            ]
            
            cmd_str = " ".join(docker_cmd)
            result = await asyncio.to_thread(ensure_command_executed, cmd_str)
            
            if result and "commissioned" in str(result).lower():
                logging.debug("✅ 커미셔닝 검증 성공")
                return True
            else:
                logging.debug("❌ 커미셔닝 검증 실패")
                return False
                
        except Exception as e:
            logging.debug(f"커미셔닝 검증 오류: {e}")
            return False


# 메인 커미셔닝 함수
async def commission_p110m_auto(commission_code: str) -> bool:
    """
    P110M 자동 커미셔닝
    
    Args:
        commission_code: Matter 커미션 코드
        
    Returns:
        bool: 성공 여부
    """
    controller = MatterCommissioningController()
    return await controller.start_commissioning_process(commission_code)


def commission_p110m_auto_sync(commission_code: str) -> bool:
    """동기 버전의 P110M 자동 커미셔닝"""
    return asyncio.run(commission_p110m_auto(commission_code))


async def test_commissioning():
    """커미셔닝 테스트"""
    logging.basicConfig(level=logging.INFO,
                      format='[%(levelname)s] %(message)s')
    
    logging.debug("P110M 커미셔닝 테스트")
    
    # 테스트용 커미션 코드 (실제 값으로 교체 필요)
    test_commission_code = "0150-093-0206"
    
    # 커미셔닝 시도
    success = await commission_p110m_auto(test_commission_code)
    
    if success:
        logging.debug("✅ 커미셔닝 테스트 성공")
    else:
        logging.debug("❌ 커미셔닝 테스트 실패")
        logging.debug("💡 수동 커미셔닝을 시도해보세요")
    
    return success


if __name__ == "__main__":
    asyncio.run(test_commissioning())
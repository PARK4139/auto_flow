#!/usr/bin/env python3

"""
Docker 기반 Matter 제어 모듈
P110M을 Docker를 통해 Matter 프로토콜로 제어합니다.
"""

import asyncio
import logging
import subprocess
import json
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


class MatterDockerController:
    """Docker 기반 Matter 제어 클래스"""
    
    def __init__(self):
        self.docker_image = "matter/matter-controller"
        self.container_name = "matter-p110m-controller"
        self.working_dir = Path("/tmp/matter_control")
    
    async def is_docker_available(self) -> bool:
        """Docker가 사용 가능한지 확인"""
        try:
            result = await asyncio.to_thread(ensure_command_executed, "docker --version")
            if result and "Docker version" in str(result):
                logging.debug("✅ Docker 사용 가능")
                return True
        except Exception as e:
            logging.debug(f"Docker 확인 실패: {e}")
        
        logging.debug("❌ Docker를 사용할 수 없습니다")
        return False
    
    async def pull_matter_image(self) -> bool:
        """Matter Docker 이미지 다운로드"""
        try:
            logging.debug("Matter Docker 이미지 다운로드 중...")
            result = await asyncio.to_thread(
                ensure_command_executed, 
                f"docker pull {self.docker_image}"
            )
            if result:
                logging.debug("✅ Matter Docker 이미지 다운로드 완료")
                return True
        except Exception as e:
            logging.debug(f"Matter 이미지 다운로드 실패: {e}")
        
        return False
    
    async def create_working_directory(self) -> bool:
        """작업 디렉토리 생성"""
        try:
            # Windows에서는 WSL을 통해 Linux 디렉토리 생성
            if self._is_windows():
                cmd = f"wsl mkdir -p {self.working_dir}"
            else:
                cmd = f"mkdir -p {self.working_dir}"
            
            await asyncio.to_thread(ensure_command_executed, cmd)
            logging.debug(f"✅ 작업 디렉토리 생성: {self.working_dir}")
            return True
        except Exception as e:
            logging.debug(f"작업 디렉토리 생성 실패: {e}")
            return False
    
    async def stop_existing_container(self) -> bool:
        """기존 컨테이너 정지 및 제거"""
        try:
            # 컨테이너 정지
            await asyncio.to_thread(
                ensure_command_executed, 
                f"docker stop {self.container_name}"
            )
            # 컨테이너 제거
            await asyncio.to_thread(
                ensure_command_executed, 
                f"docker rm {self.container_name}"
            )
            logging.debug("✅ 기존 컨테이너 정리 완료")
            return True
        except Exception as e:
            logging.debug(f"기존 컨테이너 정리 실패 (정상일 수 있음): {e}")
            return True  # 기존 컨테이너가 없을 수도 있음
    
    async def run_matter_controller(
        self, 
        commission_code: str, 
        action: str,
        device_ip: Optional[str] = None
    ) -> bool:
        """Matter 컨트롤러 컨테이너 실행"""
        try:
            # Docker 명령어 구성
            docker_cmd = [
                "docker", "run", "--rm",
                "--name", self.container_name,
                "--network", "host",  # 호스트 네트워크 사용
                "-v", f"{self.working_dir}:/workspace",
                "-w", "/workspace",
                self.docker_image,
                "matter-controller",
                "--commission-code", commission_code,
                "--action", action
            ]
            
            if device_ip:
                docker_cmd.extend(["--device-ip", device_ip])
            
            cmd_str = " ".join(docker_cmd)
            logging.debug(f"Docker 명령어 실행: {cmd_str}")
            
            result = await asyncio.to_thread(ensure_command_executed, cmd_str)
            
            if result:
                logging.debug("✅ Matter 컨트롤러 실행 완료")
                return True
                
        except Exception as e:
            logging.debug(f"Matter 컨트롤러 실행 실패: {e}")
        
        return False
    
    async def control_p110m_via_matter(
        self, 
        commission_code: str, 
        action: str,
        device_ip: Optional[str] = None
    ) -> bool:
        """P110M을 Matter 프로토콜로 제어"""
        try:
            logging.debug("🐳 Docker 기반 Matter 제어 시작")
            
            # n. Docker 사용 가능 여부 확인
            if not await self.is_docker_available():
                logging.debug("Docker를 사용할 수 없어 Matter 제어를 건너뜁니다")
                return False
            
            # n. 작업 디렉토리 생성
            if not await self.create_working_directory():
                logging.debug("작업 디렉토리 생성 실패")
                return False
            
            # n. 기존 컨테이너 정리
            await self.stop_existing_container()
            
            # n. Matter 이미지 다운로드 (필요시)
            if not await self.pull_matter_image():
                logging.debug("Matter 이미지 다운로드 실패")
                return False
            
            # n. Matter 컨트롤러 실행
            success = await self.run_matter_controller(commission_code, action, device_ip)
            
            if success:
                logging.debug("✅ Docker 기반 Matter 제어 성공")
                return True
            else:
                logging.debug("❌ Docker 기반 Matter 제어 실패")
                return False
                
        except Exception as e:
            logging.debug(f"Docker 기반 Matter 제어 중 오류: {e}")
            return False
    
    def _is_windows(self) -> bool:
        """Windows 환경인지 확인"""
        import platform
        return platform.system().lower() == "windows"


# 메인 제어 함수
async def control_p110m_via_docker_matter(
    commission_code: str,
    action: str = "toggle",
    device_ip: Optional[str] = None
) -> bool:
    """
    Docker를 통한 P110M Matter 제어
    
    Args:
        commission_code: Matter 커미션 코드
        action: 수행할 액션 ("on", "off", "toggle", "status")
        device_ip: 장치 IP (선택사항)
        
    Returns:
        bool: 성공 여부
    """
    controller = MatterDockerController()
    return await controller.control_p110m_via_matter(commission_code, action, device_ip)


def control_p110m_via_docker_matter_sync(
    commission_code: str,
    action: str = "toggle",
    device_ip: Optional[str] = None
) -> bool:
    """동기 버전의 Docker 기반 Matter 제어"""
    return asyncio.run(control_p110m_via_docker_matter(commission_code, action, device_ip))


async def test_docker_matter_control():
    """Docker 기반 Matter 제어 테스트"""
    logging.basicConfig(level=logging.INFO,
                      format='[%(levelname)s] %(message)s')
    
    logging.debug("Docker 기반 Matter 제어 테스트")
    
    # 테스트용 커미션 코드 (실제 값으로 교체 필요)
    test_commission_code = "0150-093-0206"
    
    # Docker 사용 가능 여부 확인
    controller = MatterDockerController()
    if not await controller.is_docker_available():
        logging.debug("❌ Docker를 사용할 수 없습니다")
        logging.debug("💡 해결 방법:")
        logging.debug("   1. Docker Desktop 설치")
        logging.debug("   2. Docker 서비스 시작")
        logging.debug("   3. WSL2 활성화 (Windows의 경우)")
        return False
    
    # 상태 확인 테스트
    success = await control_p110m_via_docker_matter(
        commission_code=test_commission_code,
        action="status"
    )
    
    if success:
        logging.debug("✅ Docker 기반 Matter 제어 테스트 성공")
    else:
        logging.debug("❌ Docker 기반 Matter 제어 테스트 실패")
    
    return success


if __name__ == "__main__":
    asyncio.run(test_docker_matter_control())
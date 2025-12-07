"""
Xavier에서 API 서버를 시작하는 함수
Home Assistant를 통한 장치 제어 API를 제공합니다 (플러그, TV 등)
"""

import logging
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
    PkWirelessTargetController,
    SetupOpsForPkWirelessTargetController,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def ensure_api_server_started_on_xavier(
    host: str = "0.0.0.0",
    port: int = 8000,
    xavier_ip: Optional[str] = None,
    xavier_user: Optional[str] = None,
    xavier_pw: Optional[str] = None,
) -> bool:
    """
    Xavier에서 API 서버를 시작합니다.
    
    Home Assistant를 통한 장치 제어 API를 제공합니다:
    - 플러그 제어 (P110M 등)
    - TV 제어 (media_player)
    - 엔티티 상태 조회
    
    Args:
        host: 서버 호스트. 기본값 "0.0.0.0" (모든 인터페이스)
        port: 서버 포트. 기본값 8000
        xavier_ip: Xavier IP 주소. None이면 환경변수 또는 입력받기
        xavier_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        xavier_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        
    Returns:
        bool: 서버 시작 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
        
        func_n = get_caller_name()
        
        # Xavier 연결 정보 가져오기
        if not xavier_ip:
            xavier_ip = ensure_env_var_completed_2025_11_24("XAVIER_IP", func_n=func_n)
        if not xavier_user:
            xavier_user = ensure_env_var_completed_2025_11_24("XAVIER_USER", func_n=func_n, default_value="pk")
        if not xavier_pw:
            xavier_pw = ensure_env_var_completed_2025_11_24("XAVIER_PW", func_n=func_n)
        
        # Xavier 컨트롤러 생성
        controller = PkWirelessTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            setup_op=SetupOpsForPkWirelessTargetController.TARGET,
        )
        
        # 프로젝트 내 API 서버 파일 경로
        # pk_internal_tools/pk_api_servers/pk_api_server.py
        pk_internal_tools_dir = Path(__file__).parent.parent
        local_script_path = pk_internal_tools_dir / "pk_api_servers" / "pk_api_server.py"
        
        if not local_script_path.exists():
            logger.error("API 서버 파일을 찾을 수 없습니다: %s", local_script_path)
            return False
        
        # Xavier에 API 서버 스크립트 전송
        remote_script_path = "/tmp/pk_api_server.py"
        
        try:
            logger.info("API 서버 스크립트를 Xavier에 전송 중...")
            ok = controller.ensure_file_transferred_to_target(
                str(local_script_path),
                remote_script_path,
            )
            
            if not ok:
                logger.error("스크립트 전송 실패")
                return False
            
            # Xavier에서 API 서버 실행 (백그라운드)
            logger.info("Xavier에서 API 서버를 시작합니다...")
            logger.info("서버 접속 URL: http://%s:%d", xavier_ip, port)
            logger.info("서버를 중지하려면 Xavier에서 Ctrl+C를 누르거나 프로세스를 종료하세요.")
            
            # 환경 변수 설정 및 백그라운드 실행을 위해 nohup 사용
            env_vars = f"XAVIER_API_PORT={port}"
            cmd = f"nohup env {env_vars} python3 {remote_script_path} > /tmp/pk_api_server.log 2>&1 &"
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd=cmd,
                timeout_seconds=10,
                use_sudo=False,
            )
            
            if exit_code == 0:
                logger.info("✅ API 서버가 Xavier에서 시작되었습니다.")
                logger.info("🌐 접속 URL: http://%s:%d", xavier_ip, port)
                logger.info("📋 API 문서: http://%s:%d/docs", xavier_ip, port)
                logger.info("서버 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/pk_api_server.log'")
                logger.info("서버 중지: Xavier에서 'pkill -f pk_api_server.py'")
                return True
            else:
                logger.error("API 서버 시작 실패")
                if stderr:
                    for line in stderr:
                        logger.error("  %s", line)
                return False
        
        except Exception as inner_e:
            logger.error("스크립트 전송 또는 서버 시작 중 오류 발생: %s", inner_e, exc_info=True)
            return False
    
    except Exception as e:
        logger.error(f"Xavier API 서버 시작 중 예외 발생: {e}", exc_info=True)
        return False







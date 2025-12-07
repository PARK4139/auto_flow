"""
대시보드 웹 서버를 시작하는 함수.
FastAPI 기반으로 반응형 웹 대시보드를 제공합니다.
Windows/Linux 모두 지원.
"""
import logging
import socket
from pathlib import Path
from typing import Optional
import uvicorn


def get_local_ip() -> str:
    """
    로컬 IP 주소를 가져옵니다 (Windows/Linux 호환).
    
    Returns:
        str: 로컬 IP 주소
    """
    try:
        # 외부 연결을 시도하여 로컬 IP 확인
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            # 대체 방법
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return "127.0.0.1"


def ensure_pk_dashboard_server_started(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False
) -> None:
    """
    대시보드 웹 서버를 시작합니다 (Windows/Linux 호환).
    
    Args:
        host: 서버 호스트. 기본값 "0.0.0.0" (모든 인터페이스)
        port: 서버 포트. 기본값 8000
        reload: 개발 모드 (자동 리로드). 기본값 False
    """
    try:
        from pk_internal_tools.pk_functions.pk_dashboard_server import app
        
        local_ip = get_local_ip()
        
        logging.info("=" * 60)
        logging.info("🌡️ PK System Dashboard 서버 시작")
        logging.info("=" * 60)
        logging.info(f"📱 모바일 접속: http://{local_ip}:{port}")
        logging.info(f"💻 PC 접속: http://localhost:{port}")
        logging.info(f"🌐 네트워크 접속: http://{host if host != '0.0.0.0' else local_ip}:{port}")
        logging.info("=" * 60)
        logging.info("서버를 중지하려면 Ctrl+C를 누르세요.")
        logging.info("=" * 60)
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        logging.error(f"대시보드 서버 시작 실패: {e}")
        raise


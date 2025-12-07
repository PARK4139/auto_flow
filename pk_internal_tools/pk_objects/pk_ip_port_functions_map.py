#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP와 포트를 기능별로 매핑하는 클래스

서버 추가 시 추가 작성, 서버 기능 설명을 상세히 작성하세요.

사용 방법:
    1. ServerFunctionName Enum에 새 기능 추가 (필요시)
    2. ServerFunctionConfig dataclass로 기능 상세 정보 정의
    3. 각 서버 딕셔너리에 기능 추가
    4. 상세한 주석과 docstring 작성 필수
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class ServerFunctionName(str, Enum):
    """
    서버 기능 이름 Enum
    
    새로운 기능 추가 시:
    1. 이 Enum에 기능 이름 추가
    2. ServerFunctionConfig로 상세 정보 정의
    3. 각 서버 딕셔너리에 추가
    
    예시:
        NEW_FEATURE = "new_feature"
    """
    DASHBOARD = "dashboard"
    SSH = "ssh"
    MONITOR = "monitor"
    ARDUINO_DEV = "arduino_dev"
    VSCODE = "vscode"
    # 새로운 기능 추가 시 여기에 Enum 값 추가


@dataclass
class ServerFunctionConfig:
    """
    서버 기능 설정 데이터 클래스
    
    각 서버 기능의 상세 정보를 구조화된 형태로 저장합니다.
    
    Attributes:
        ip: IP 주소 (None인 경우 environment_var에서 자동으로 가져옴)
        port: 포트 번호 (None인 경우 포트가 없는 서비스)
        function_description: 기능에 대한 상세 설명 (필수, 여러 줄 가능)
        protocol: 사용 프로토콜 (http, https, ssh, tcp, udp, local, process 등)
        environment_var: IP를 가져올 환경변수 이름 (None이면 ip 값 사용)
        additional_info: 추가 정보 딕셔너리 (선택사항)
            - framework: 사용 프레임워크
            - log_file: 로그 파일 경로
            - db_path: 데이터베이스 경로
            - 기타 서비스별 특수 정보
    
    Examples:
        >>> config = ServerFunctionConfig(
        ...     ip=None,
        ...     port=8000,
        ...     function_description="대시보드 서버\n- 기능: ...\n- 접속: ...",
        ...     protocol="http",
        ...     environment_var="XAVIER_IP",
        ...     additional_info={"framework": "FastAPI"}
        ... )
    """
    ip: Optional[str] = None
    port: Optional[int] = None
    function_description: str = ""
    protocol: str = "http"
    environment_var: Optional[str] = None
    additional_info: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """초기화 후 검증"""
        if not self.function_description:
            logger.warning(
                "function_description이 비어있습니다. "
                "상세한 설명을 작성해주세요:\n"
                "- 기능 설명\n"
                "- 접속 방법\n"
                "- 시작/중지 방법\n"
                "- 관련 파일 경로"
            )


class pk_ip_port_functions_map:
    """
    서버별 IP, 포트, 기능 설명 매핑 클래스
    
    서버 추가 시:
    1. ServerFunctionName Enum에 기능 추가 (필요시)
    2. ServerFunctionConfig로 각 기능의 상세 정보 정의
    3. 해당 서버의 딕셔너리에 기능 추가
    4. 서버 섹션 위에 상세한 주석 블록 작성 (=== 구분선 사용)
    
    각 서버 설정은 반드시 상세한 주석과 함께 작성하세요:
    - 서버의 물리적/논리적 위치
    - 서버의 주요 용도
    - 접속 방법
    - 기능별 상세 설명
    """
    
    # ============================================================================
    # pk_xavier 서버 설정
    # ============================================================================
    # 
    # 서버 정보:
    #   - 이름: pk_xavier (Jetson AGX Xavier)
    #   - 위치: 물리적 위치 또는 네트워크 위치 (예: 사무실, 집 등)
    #   - 용도: P110M 제어, 에너지 모니터링, Arduino 개발 환경
    #   - OS: Ubuntu (JetPack 기반)
    #   - 접속: SSH, 웹 대시보드
    # 
    # 기능별 상세 설명:
    #   - dashboard: P110M 스마트 플러그의 에너지 사용량을 그래프로 시각화하고
    #               웹 인터페이스를 통해 원격 제어(ON/OFF/Toggle/Info/Energy)를 제공합니다.
    #               FastAPI 기반으로 구현되어 있으며, Xavier에서 실행됩니다.
    #               Host Machine에서 Xavier IP로 접속 가능합니다.
    #   - ssh: Xavier에 원격 접속하여 명령어 실행 및 파일 관리
    #          VSCode Remote SSH를 통해 호스트 머신에서 코드 작성 가능
    #   - monitor: P110M 에너지 데이터를 주기적으로 수집하여 SQLite DB에 저장
    #              백그라운드 프로세스로 실행되며, nohup으로 관리됩니다.
    #              모니터링 간격은 60초, 300초, 600초, 1800초 중 선택 가능합니다.
    #   - arduino_dev: PlatformIO 기반 Arduino 개발 환경
    #                  VSCode Remote SSH를 통해 호스트 머신에서 코드 작성 및 업로드
    #                  지원 보드: Arduino Uno, Nano, Nano ESP32, ESP32 Dev
    #
    pk_xavier: Dict[str, ServerFunctionConfig] = {
        ServerFunctionName.DASHBOARD.value: ServerFunctionConfig(
            ip=None,  # 환경변수 XAVIER_IP에서 자동으로 가져옴
            port=8000,
            function_description=(
                "P110M 대시보드 및 제어 웹 서버\n"
                "- 기능: 에너지 사용량 그래프 시각화, 원격 제어 (ON/OFF/Toggle/Info/Energy)\n"
                "- 기술: FastAPI + Uvicorn + Plotly.js\n"
                "- 접속: http://{XAVIER_IP}:8000\n"
                "- 시작: wireless 액션 > 'execute P110M dashboard and control web server on Xavier'\n"
                "- 중지: Xavier에서 'pkill -f ensure_pk_p110m_pk_dashboard_server_on_xavier.py'\n"
                "- 로그: /tmp/p110m_pk_dashboard_server.log\n"
                "- DB: ~/pk_system/.pk_system/pk_system.sqlite"
            ),
            protocol="http",
            environment_var="XAVIER_IP",
            additional_info={
                "framework": "FastAPI",
                "log_file": "/tmp/p110m_pk_dashboard_server.log",
                "db_path": "~/pk_system/.pk_system/pk_system.sqlite",
                "start_command": "nohup python3 /tmp/ensure_pk_p110m_pk_dashboard_server_on_xavier.py",
                "stop_command": "pkill -f ensure_pk_p110m_pk_dashboard_server_on_xavier.py"
            }
        ),
        ServerFunctionName.SSH.value: ServerFunctionConfig(
            ip=None,  # 환경변수 XAVIER_IP에서 자동으로 가져옴
            port=22,
            function_description=(
                "SSH 원격 접속\n"
                "- 기능: Xavier에 원격 접속하여 명령어 실행 및 파일 관리\n"
                "- 접속: ssh {XAVIER_USER}@{XAVIER_IP}\n"
                "- VSCode Remote SSH: F1 > 'Remote-SSH: Connect to Host' > '{XAVIER_USER}@{XAVIER_IP}'\n"
                "- 인증: SSH 키 기반 인증 (비밀번호 입력 최소화)\n"
                "- 기본 사용자: pk"
            ),
            protocol="ssh",
            environment_var="XAVIER_IP",
            additional_info={
                "default_user": "pk",
                "key_auth": True,
                "vscode_remote": True
            }
        ),
        ServerFunctionName.MONITOR.value: ServerFunctionConfig(
            ip=None,  # 환경변수 XAVIER_IP에서 자동으로 가져옴
            port=None,  # 백그라운드 프로세스
            function_description=(
                "P110M 에너지 모니터링 (백그라운드 프로세스)\n"
                "- 기능: P110M 에너지 데이터를 주기적으로 수집하여 SQLite DB에 저장\n"
                "- 실행: wireless 액션 > 'execute P110M monitor on Xavier'\n"
                "- 간격: 60초, 300초, 600초, 1800초 중 선택\n"
                "- 로그: /tmp/p110m_monitor.log\n"
                "- 중지: Xavier에서 'pkill -f ensure_pk_p110m_monitor_on_xavier.py'\n"
                "- DB: ~/pk_system/.pk_system/pk_system.sqlite\n"
                "- 데이터: current_power, today_energy, month_energy 등"
            ),
            protocol="process",
            environment_var="XAVIER_IP",
            additional_info={
                "log_file": "/tmp/p110m_monitor.log",
                "db_path": "~/pk_system/.pk_system/pk_system.sqlite",
                "intervals": [60, 300, 600, 1800],
                "start_command": "nohup python3 /tmp/ensure_pk_p110m_monitor_on_xavier.py",
                "stop_command": "pkill -f ensure_pk_p110m_monitor_on_xavier.py",
                "process_type": "background"
            }
        ),
        ServerFunctionName.ARDUINO_DEV.value: ServerFunctionConfig(
            ip=None,  # 환경변수 XAVIER_IP에서 자동으로 가져옴
            port=None,  # VSCode Remote SSH 사용
            function_description=(
                "Arduino 개발 환경 (VSCode Remote SSH)\n"
                "- 기능: PlatformIO 기반 Arduino 및 개발 보드 개발 환경\n"
                "- 기술: VSCode + PlatformIO + platformio.ini\n"
                "- 설정: wired 액션 > 'Arduino dev via wired Xavier wireless Arduino'\n"
                "- 접속: VSCode Remote SSH로 Xavier 연결 후 PlatformIO 확장 설치\n"
                "- 프로젝트: ~/arduino_projects\n"
                "- 기본 타겟: Arduino Nano (ATmega328P) + ESP8266 + esp-link (Wi-Fi↔UART bridge)\n"
                "- Wired 타겟: Arduino Nano (ATmega328P) - USB 케이블 직접 연결\n"
                "- 지원 보드: Nano+ESP8266+esp-link, Nano(wired), Uno, Nano ESP32, ESP32 Dev\n"
                "- USB 접근: dialout 그룹 권한 필요 (재로그인 또는 재부팅 후 적용)\n"
                "- 플랫폼: PlatformIO Core (Python 기반)\n"
                "- 연결 구조: pk_asus (wired) - Xavier (wireless) - Arduino"
            ),
            protocol="ssh",
            environment_var="XAVIER_IP",
            additional_info={
                "project_dir": "~/arduino_projects",
                "platformio_path": "~/.local/bin",
                "default_target": "nano_esp8266_esplink",
                "supported_boards": ["nano_esp8266_esplink", "uno", "nano", "nano_esp32", "esp32dev"],
                "vscode_extension": "platformio.platformio-ide",
                "udev_rules": "/etc/udev/rules.d/99-platformio-udev.rules",
                "esp_link_github": "https://github.com/jeelabs/esp-link"
            }
        ),
    }
    
    # ============================================================================
    # pk_asus 서버 설정
    # ============================================================================
    # 
    # 서버 정보:
    #   - 이름: pk_asus (Host Machine)
    #   - 위치: 개발 머신 (현재 PC)
    #   - 용도: 로컬 개발, 대시보드 서버, WSL 관리
    #   - OS: Windows 11 + WSL2 Ubuntu
    #   - 접속: localhost, SSH (WSL)
    # 
    # 기능별 상세 설명:
    #   - dashboard: PK System 전체 대시보드 (기온, 시스템 정보, P110M 에너지 등)
    #                FastAPI 기반으로 구현되어 있으며, 로컬에서만 접속 가능합니다.
    #   - ssh: WSL Ubuntu에 SSH 접속
    #          VSCode Remote SSH를 통해 WSL에 연결 가능
    #   - vscode: 로컬 VSCode 개발 환경
    #             확장 프로그램: Remote-SSH, PlatformIO, Python 등
    #
    pk_asus: Dict[str, ServerFunctionConfig] = {
        ServerFunctionName.DASHBOARD.value: ServerFunctionConfig(
            ip="localhost",
            port=8000,
            function_description=(
                "PK System 대시보드 서버\n"
                "- 기능: 기온, 시스템 정보, P110M 에너지 사용량 등 통합 대시보드\n"
                "- 기술: FastAPI + Uvicorn + Plotly.js\n"
                "- 접속: http://localhost:8000\n"
                "- 시작: python -m pk_internal_tools.pk_wrappers.pk_ensure_pk_dashboard_server_started\n"
                "- 로컬 전용: localhost에서만 접속 가능"
            ),
            protocol="http",
            additional_info={
                "framework": "FastAPI",
                "local_only": True,
                "start_command": "python -m pk_internal_tools.pk_wrappers.pk_ensure_pk_dashboard_server_started"
            }
        ),
        ServerFunctionName.SSH.value: ServerFunctionConfig(
            ip="localhost",
            port=22,
            function_description=(
                "SSH 원격 접속 (WSL)\n"
                "- 기능: WSL Ubuntu에 SSH 접속\n"
                "- 접속: ssh {WSL_USER}@localhost -p {WSL_PORT}\n"
                "- VSCode Remote SSH: F1 > 'Remote-SSH: Connect to Host' > 'WSL'\n"
                "- 대상: WSL2 Ubuntu 배포판"
            ),
            protocol="ssh",
            additional_info={
                "target": "WSL Ubuntu",
                "key_auth": True,
                "vscode_remote": True
            }
        ),
        ServerFunctionName.VSCODE.value: ServerFunctionConfig(
            ip="localhost",
            port=None,  # VSCode 자체 포트
            function_description=(
                "VSCode 로컬 개발 환경\n"
                "- 기능: 로컬 파일 편집, 디버깅, 확장 프로그램 사용\n"
                "- 접속: VSCode 직접 실행\n"
                "- 확장: Remote-SSH, PlatformIO, Python, Docker 등\n"
                "- 위치: Windows 호스트 머신"
            ),
            protocol="local",
            additional_info={
                "type": "local_editor",
                "extensions": [
                    "Remote-SSH",
                    "PlatformIO",
                    "Python",
                    "Docker",
                    "Git"
                ]
            }
        ),
    }
    
    @classmethod
    def get_server_info(cls, server_name: str, function_name: str) -> Optional[ServerFunctionConfig]:
        """
        서버와 기능에 해당하는 설정 정보를 반환합니다.
        
        Args:
            server_name: 서버 이름 (예: "pk_xavier", "pk_asus")
            function_name: 기능 이름 (예: "dashboard", "ssh") 또는 ServerFunctionName Enum 값
            
        Returns:
            ServerFunctionConfig: 서버 기능 설정 객체 또는 None
        """
        if not hasattr(cls, server_name):
            logger.warning("서버를 찾을 수 없습니다: %s", server_name)
            logger.info("사용 가능한 서버: %s", cls.list_all_servers())
            return None
        
        server_dict = getattr(cls, server_name)
        if not isinstance(server_dict, dict):
            logger.warning("서버 설정이 딕셔너리가 아닙니다: %s", server_name)
            return None
        
        # Enum 값이면 value로 변환
        if isinstance(function_name, ServerFunctionName):
            function_name = function_name.value
        
        if function_name not in server_dict:
            logger.warning("기능을 찾을 수 없습니다: %s.%s", server_name, function_name)
            logger.info("사용 가능한 기능: %s", list(server_dict.keys()))
            return None
        
        return server_dict[function_name]
    
    @classmethod
    def get_all_functions(cls, server_name: str) -> Optional[Dict[str, ServerFunctionConfig]]:
        """
        서버의 모든 기능 목록을 반환합니다.
        
        Args:
            server_name: 서버 이름 (예: "pk_xavier", "pk_asus")
            
        Returns:
            Dict[str, ServerFunctionConfig]: 모든 기능 딕셔너리 또는 None
        """
        if not hasattr(cls, server_name):
            logger.warning("서버를 찾을 수 없습니다: %s", server_name)
            logger.info("사용 가능한 서버: %s", cls.list_all_servers())
            return None
        
        server_dict = getattr(cls, server_name)
        if not isinstance(server_dict, dict):
            logger.warning("서버 설정이 딕셔너리가 아닙니다: %s", server_name)
            return None
        
        return server_dict
    
    @classmethod
    def resolve_ip(cls, server_name: str, function_name: str, default_ip: Optional[str] = None) -> Optional[str]:
        """
        서버의 IP 주소를 해석합니다 (환경변수에서 가져오거나 기본값 사용).
        
        Args:
            server_name: 서버 이름 (예: "pk_xavier", "pk_asus")
            function_name: 기능 이름 (예: "dashboard", "ssh")
            default_ip: 기본 IP 주소 (None인 경우 환경변수에서 가져옴)
            
        Returns:
            str: IP 주소 또는 None
        """
        info = cls.get_server_info(server_name, function_name)
        if not info:
            return default_ip
        
        ip = info.ip
        
        # IP가 None이면 환경변수에서 가져오기
        if ip is None:
            env_var = info.environment_var
            if env_var:
                try:
                    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
                    ip = ensure_env_var_completed_2025_11_24(env_var, default_value=default_ip)
                except Exception as e:
                    logger.warning("%s 환경변수를 가져올 수 없습니다: %s", env_var, e)
                    ip = default_ip
            elif server_name == "pk_asus":
                ip = default_ip or "localhost"
            else:
                ip = default_ip
        
        return ip
    
    @classmethod
    def get_url(cls, server_name: str, function_name: str, protocol: str = "http", default_ip: Optional[str] = None) -> Optional[str]:
        """
        서버의 기능에 대한 URL을 생성합니다.
        
        Args:
            server_name: 서버 이름 (예: "pk_xavier", "pk_asus")
            function_name: 기능 이름 (예: "dashboard", "ssh")
            protocol: 프로토콜 (예: "http", "https", "ssh")
            default_ip: 기본 IP 주소
            
        Returns:
            str: URL 또는 None
        """
        info = cls.get_server_info(server_name, function_name)
        if not info:
            return None
        
        # protocol이 지정되지 않았으면 config에서 가져오기
        if protocol == "http" and info.protocol != "http":
            protocol = info.protocol
        
        ip = cls.resolve_ip(server_name, function_name, default_ip)
        port = info.port
        
        if not ip:
            return None
        
        if port is None:
            if protocol in ["ssh", "local", "process"]:
                if protocol == "ssh":
                    return f"{protocol}://{ip}"
                return None
            return None
        
        if protocol == "ssh":
            return f"{protocol}://{ip}:{port}"
        else:
            return f"{protocol}://{ip}:{port}"
    
    @classmethod
    def list_all_servers(cls) -> list:
        """
        등록된 모든 서버 목록을 반환합니다.
        
        Returns:
            list: 서버 이름 목록
        """
        servers = []
        for attr_name in dir(cls):
            if not attr_name.startswith("_") and attr_name not in ["get_server_info", "get_all_functions", "resolve_ip", "get_url", "list_all_servers"]:
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, dict):
                    servers.append(attr_name)
        return servers

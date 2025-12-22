"""
Xavier에서 Arduino로 개발 코드 무선 전송 (wireless programming)
Wi-Fi↔UART bridge 또는 OTA를 통한 무선 코드 업로드
"""
import logging
import textwrap
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)

logger = logging.getLogger(__name__)


def _get_wireless_code_upload_guide() -> str:
    """wireless 코드 업로드 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    Wireless 프로그래밍: Xavier → Arduino 코드 전송
    ========================================
    
    ## 연결 구조
    
    ```
    Xavier
      ↓ [Wi-Fi]
    ESP8266 (esp-link 또는 OTA 에이전트)
      ↓ [UART 또는 OTA]
    Arduino Nano (ATmega328P)
    ```
    
    ## 방법 1: OTA를 통한 직접 업로드 (권장)
    
    ### 사전 요구사항:
    - ESP8266에 OTA 에이전트가 설치되어 있어야 함
    - ESP8266이 Wi-Fi에 연결되어 있어야 함
    - ESP8266 IP 주소 확인 필요
    
    ### PlatformIO OTA 업로드:
    ```ini
    [env:nodemcuv2]
    platform = espressif8266
    board = nodemcuv2
    framework = arduino
    upload_protocol = espota
    upload_port = <esp8266_ip>
    upload_flags = 
        --auth=ota_password
    ```
    
    ### 업로드 명령:
    ```bash
    cd ~/arduino_projects/<project_dir>
    python3 -m platformio run --target upload
    ```
    
    ## 방법 2: esp-link를 통한 시리얼 모니터 (디버깅용)
    
    ### esp-link TCP/Telnet:
    ```bash
    # 시리얼 모니터
    telnet <esp8266_ip> 23
    
    # 또는 netcat
    nc <esp8266_ip> 23
    ```
    
    ### HTTP API를 통한 제어:
    ```bash
    # GPIO 제어
    curl http://<esp8266_ip>/v1/pin/13/1
    curl http://<esp8266_ip>/v1/pin/13/0
    
    # 상태 확인
    curl http://<esp8266_ip>/status
    ```
    
    ## 방법 3: 코드 파일 전송 후 로컬 컴파일
    
    ### Xavier에서 코드 작성:
    1. VSCode Remote SSH로 remote_target 연결
    2. ~/arduino_projects에서 코드 작성
    3. PlatformIO로 컴파일
    
    ### 무선 업로드:
    ```bash
    # OTA 업로드
    python3 -m platformio run --target upload --upload-port <esp8266_ip>
    ```
    
    ## 문제 해결
    
    ### OTA 업로드 실패:
    1. ESP8266 IP 주소 확인
    2. 같은 Wi-Fi 네트워크 확인
    3. OTA 비밀번호 확인
    4. ESP8266이 OTA 모드인지 확인
    
    ### 연결 안 됨:
    1. ping 테스트: `ping <esp8266_ip>`
    2. 시리얼 모니터로 ESP8266 상태 확인
    3. 방화벽 설정 확인
    
    ========================================
    """)


def ensure_development_code_uploaded_from_remote_target_to_arduino_wireless(
        remote_target_ip: Optional[str] = None,
        remote_target_user: Optional[str] = None,
        remote_target_pw: Optional[str] = None,
        esp8266_ip: Optional[str] = None,
        project_path: Optional[str] = None,
        ota_password: Optional[str] = None,
) -> bool:
    """
    Xavier에서 Arduino로 개발 코드를 무선으로 전송합니다.
    
    Wi-Fi↔UART bridge 또는 OTA를 통한 무선 프로그래밍을 지원합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        esp8266_ip: ESP8266 IP 주소. None이면 입력받기
        project_path: PlatformIO 프로젝트 경로. None이면 입력받기
        ota_password: OTA 업로드 비밀번호. None이면 입력받기
        
    Returns:
        bool: 업로드 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed

        func_n = get_caller_name()

        logger.info("=" * 60)
        logger.info("Wireless 프로그래밍: Xavier → Arduino 코드 전송")
        logger.info("=" * 60)

        # 가이드 표시
        logger.info(_get_wireless_code_upload_guide())

        # 1. remote_target 연결 정보 가져오기
        if not remote_target_ip:
            remote_target_ip = ensure_env_var_completed("XAVIER_IP")
        if not remote_target_user:
            remote_target_user = ensure_env_var_completed("XAVIER_USER")
        if not remote_target_pw:
            remote_target_pw = ensure_env_var_completed("XAVIER_PW")

        # 2. Xavier 컨트롤러 생성
        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier,
            
        )

        # 3. ESP8266 IP 주소 확인
        logger.info("1. ESP8266 IP 주소 확인 중...")
        if not esp8266_ip:
            esp8266_ip = ensure_env_var_completed(
                "ESP8266_IP",
                func_n=func_n,
                guide_text="ESP8266의 IP 주소를 입력하세요 (예: 192.168.0.100):",
            )

        if not esp8266_ip:
            logger.error("ESP8266 IP 주소가 입력되지 않았습니다.")
            return False

        # 4. ESP8266 연결 확인
        logger.info("2. ESP8266 연결 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=f"ping -c 3 {esp8266_ip}",
            timeout_seconds=10,
            use_sudo=False,
        )
        if exit_code == 0:
            logger.info("  ✅ ESP8266에 ping 성공")
        else:
            logger.warning("  ⚠️ ESP8266에 ping 실패")
            logger.info("  ESP8266이 Wi-Fi에 연결되어 있는지 확인하세요.")
            return False

        # 5. 프로젝트 경로 확인
        logger.info("3. PlatformIO 프로젝트 경로 확인 중...")
        if not project_path:
            project_path = ensure_env_var_completed(
                "ARDUINO_PROJECT_PATH",
                func_n=func_n,
                guide_text="PlatformIO 프로젝트 경로를 입력하세요 (예: ~/arduino_projects/my_project):",
            )

        if not project_path:
            logger.error("프로젝트 경로가 입력되지 않았습니다.")
            return False

        # 6. OTA 비밀번호 확인 (필요한 경우)
        if not ota_password:
            ota_password_input = ensure_env_var_completed(
                "OTA_PASSWORD",
                func_n=func_n,
                guide_text="OTA 업로드 비밀번호를 입력하세요 (설정하지 않은 경우 Enter):",
            )
            ota_password = ota_password_input if ota_password_input else None

        # 7. PlatformIO OTA 업로드 실행
        logger.info("4. PlatformIO OTA 업로드 실행 중...")
        logger.info("  프로젝트: %s", project_path)
        logger.info("  ESP8266 IP: %s", esp8266_ip)

        # platformio.ini에 OTA 설정 추가 확인
        logger.info("  platformio.ini에 다음 설정이 필요합니다:")
        logger.info("    upload_protocol = espota")
        logger.info("    upload_port = %s", esp8266_ip)
        if ota_password:
            logger.info("    upload_flags = --auth=%s", ota_password)

        # 업로드 명령 실행
        upload_cmd = f"cd {project_path} && python3 -m platformio run --target upload"
        if ota_password:
            upload_cmd += f" --upload-port {esp8266_ip} --upload-flags '--auth={ota_password}'"
        else:
            upload_cmd += f" --upload-port {esp8266_ip}"

        logger.info("  실행 명령: %s", upload_cmd)
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=upload_cmd,
            timeout_seconds=120,  # 업로드는 시간이 걸릴 수 있음
            use_sudo=False,
        )

        if exit_code == 0:
            logger.info("  ✅ OTA 업로드 성공")
            if stdout:
                for line in stdout[-10:]:  # 마지막 10줄만 출력
                    logger.info("    %s", line)
        else:
            logger.error("  ❌ OTA 업로드 실패")
            if stderr:
                for line in stderr:
                    logger.error("    %s", line)
            return False

        # 8. 최종 안내
        logger.info("=" * 60)
        logger.info("✅ Wireless 코드 업로드 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. 시리얼 모니터로 동작 확인:")
        logger.info("   telnet %s 23", esp8266_ip)
        logger.info("2. 또는 PlatformIO 시리얼 모니터:")
        logger.info("   python3 -m platformio device monitor --port tcp://%s:23", esp8266_ip)
        logger.info("")
        logger.info("⚠️ 참고:")
        logger.info("- OTA 업로드는 ESP8266에 OTA 에이전트가 설치되어 있어야 합니다.")
        logger.info("- esp-link만으로는 OTA 업로드가 불가능합니다.")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("Wireless 코드 업로드 중 예외 발생: %s", e, exc_info=True)
        return False

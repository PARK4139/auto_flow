"""
Arduino 개발 환경 설정 (Xavier - wired - Arduino Nano)
Xavier에서 USB 케이블로 Arduino Nano에 직접 연결하여 개발하는 기능
무선 모듈 없이 USB 시리얼 연결로 개발 가능
"""
import logging
import textwrap
from pathlib import Path
from typing import Optional, List, Dict

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
    PkWirelessTargetController,
    SetupOpsForPkWirelessTargetController,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def _get_wired_arduino_dev_guide() -> str:
    """wired Arduino 개발 환경 설정 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    Arduino Nano Wired 개발 환경 설정 가이드
    ========================================
    
    ## 연결 구조
    Xavier - wired (USB) - Arduino Nano
    
    ## 1단계: 하드웨어 연결
    
    ### USB 케이블 연결:
    1. Arduino Nano를 USB 케이블로 Xavier의 USB 포트에 연결
    2. Arduino Nano의 전원 LED가 켜지는지 확인
    3. USB 케이블이 데이터 전송을 지원하는지 확인 (충전 전용 케이블 제외)
    
    ### 연결 확인:
    ```bash
    # USB 장치 확인
    lsusb | grep -i "arduino\|ch340\|cp210\|ft232"
    
    # 시리얼 포트 확인
    ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
    
    # 또는
    dmesg | tail -20 | grep -i "tty\|usb\|serial"
    ```
    
    ## 2단계: USB 시리얼 장치 확인
    
    ### 일반적인 시리얼 포트:
    - `/dev/ttyUSB0` - CH340, CP2102 등 USB-to-Serial 칩
    - `/dev/ttyACM0` - Arduino Uno/Nano (ATmega16U2)
    
    ### 장치 확인:
    ```bash
    # 시리얼 포트 목록
    ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
    
    # 장치 권한 확인
    ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
    
    # 사용자가 dialout 그룹에 속해있는지 확인
    groups | grep dialout
    ```
    
    ## 3단계: PlatformIO 개발 환경 설정
    
    ### 프로젝트 디렉토리:
    ```bash
    cd ~/arduino_projects
    ```
    
    ### PlatformIO 프로젝트 생성:
    ```bash
    # Arduino Nano 프로젝트 생성
    python3 -m platformio project init --board nanoatmega328 --project-dir nano_wired_project
    ```
    
    ### platformio.ini 설정:
    ```ini
    [platformio]
    default_envs = nano_standalone
    
    [env:nano_standalone]
    platform = atmelavr
    board = nanoatmega328
    framework = arduino
    monitor_speed = 115200
    
    ; USB 시리얼 포트 지정 (선택사항)
    ; monitor_port = /dev/ttyUSB0
    ; upload_port = /dev/ttyUSB0
    ```
    
    ## 4단계: 코드 업로드 및 시리얼 모니터
    
    ### 코드 업로드:
    ```bash
    cd ~/arduino_projects/nano_wired_project
    python3 -m platformio run --target upload
    ```
    
    ### 시리얼 모니터:
    ```bash
    # PlatformIO 시리얼 모니터
    python3 -m platformio device monitor
    
    # 또는 직접 시리얼 포트 사용
    screen /dev/ttyUSB0 115200
    # 종료: Ctrl+A, K, Y
    ```
    
    ## 5단계: VSCode Remote SSH로 개발
    
    ### VSCode 설정:
    1. VSCode에서 Remote-SSH 확장 설치
    2. F1 > 'Remote-SSH: Connect to Host'
    3. 'pk@<xavier_ip>' 입력
    4. PlatformIO 확장 설치
    5. 프로젝트 디렉토리 열기: ~/arduino_projects
    
    ### PlatformIO 작업:
    - Upload: Ctrl+Alt+U 또는 PlatformIO: Upload
    - Serial Monitor: PlatformIO: Serial Monitor
    - Clean: PlatformIO: Clean
    
    ## 문제 해결
    
    ### USB 장치가 인식되지 않는 경우:
    1. USB 케이블 확인 (데이터 전송 지원 여부)
    2. USB 포트 변경 시도
    3. USB 장치 확인:
       ```bash
       lsusb
       dmesg | tail -30
       ```
    4. 드라이버 확인:
       - CH340: `sudo apt-get install -y ch340-dkms`
       - CP2102: 일반적으로 자동 인식
    
    ### 권한 문제:
    1. dialout 그룹 확인: `groups | grep dialout`
    2. 그룹에 추가 (이미 온보딩에서 수행됨):
       ```bash
       sudo usermod -a -G dialout $USER
       ```
    3. 재로그인 또는 재부팅 필요
    
    ### 업로드 실패:
    1. 시리얼 포트 확인: `ls /dev/ttyUSB* /dev/ttyACM*`
    2. platformio.ini에 포트 지정:
       ```ini
       upload_port = /dev/ttyUSB0
       ```
    3. 보드 리셋 버튼 누른 후 업로드 시도
    4. 다른 프로그램이 시리얼 포트를 사용 중인지 확인:
       ```bash
       lsof /dev/ttyUSB0
       ```
    
    ### 시리얼 모니터가 작동하지 않는 경우:
    1. Baud rate 확인 (기본값: 115200)
    2. 시리얼 포트 확인
    3. Arduino 스케치의 Serial.begin() 속도 확인
    
    ========================================
    """)


def _check_usb_serial_devices_on_xavier(controller: PkWirelessTargetController) -> List[Dict[str, str]]:
    """Xavier에서 USB 시리얼 장치 확인"""
    logger.info("Xavier에서 USB 시리얼 장치 확인 중...")
    
    devices = []
    
    # 1. USB 장치 확인
    logger.info("1. USB 장치 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd="lsusb | grep -i 'arduino\\|ch340\\|cp210\\|ft232\\|serial' || echo 'USB 시리얼 장치 미감지'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            logger.info("  %s", line)
            if "미감지" not in line:
                devices.append({"type": "usb", "info": line.strip()})
    
    # 2. 시리얼 포트 확인
    logger.info("2. 시리얼 포트 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd="ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || echo '시리얼 포트 없음'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            logger.info("  %s", line)
            if "시리얼 포트 없음" not in line and "tty" in line:
                # 포트 경로 추출
                parts = line.split()
                if len(parts) >= 9:
                    port_path = parts[-1]
                    if port_path.startswith("/dev/tty"):
                        devices.append({"type": "serial_port", "path": port_path, "info": line.strip()})
    
    # 3. dialout 그룹 확인
    logger.info("3. 사용자 그룹 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd="groups | grep -q dialout && echo 'dialout 그룹에 속함' || echo 'dialout 그룹에 속하지 않음'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            logger.info("  %s", line)
    
    return devices


def ensure_arduino_dev_via_wired_xavier_wired_arduino_nano(
    xavier_ip: Optional[str] = None,
    xavier_user: Optional[str] = None,
    xavier_pw: Optional[str] = None,
) -> bool:
    """
    Xavier에서 USB 케이블로 Arduino Nano에 직접 연결하여 개발 환경을 설정합니다.
    
    Args:
        xavier_ip: Xavier IP 주소. None이면 환경변수 또는 입력받기
        xavier_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        xavier_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        
    Returns:
        bool: 설정 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
        from pk_internal_tools.pk_functions.ensure_arduino_dev_environment_onboarded_on_xavier import (
            ensure_arduino_dev_environment_onboarded_on_xavier,
        )
        
        func_n = get_caller_name()
        
        logger.info("=" * 60)
        logger.info("Arduino Nano Wired 개발 환경 설정 시작")
        logger.info("구조: Xavier (wired USB) - Arduino Nano")
        logger.info("=" * 60)
        
        # 가이드 표시
        logger.info(_get_wired_arduino_dev_guide())
        
        # 1. Xavier 연결 정보 가져오기
        if not xavier_ip:
            xavier_ip = ensure_env_var_completed_2025_11_24("XAVIER_IP", func_n=func_n)
        if not xavier_user:
            xavier_user = ensure_env_var_completed_2025_11_24("XAVIER_USER", func_n=func_n, default_value="pk")
        if not xavier_pw:
            xavier_pw = ensure_env_var_completed_2025_11_24("XAVIER_PW", func_n=func_n)
        
        # 2. Xavier 컨트롤러 생성
        controller = PkWirelessTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            setup_op=SetupOpsForPkWirelessTargetController.TARGET,
        )
        
        # 3. Arduino 개발 환경 온보딩 (이미 되어있을 수 있음)
        logger.info("1. Arduino 개발 환경 확인 중...")
        success = ensure_arduino_dev_environment_onboarded_on_xavier(
            xavier_ip=xavier_ip,
            xavier_user=xavier_user,
            xavier_pw=xavier_pw,
        )
        
        if not success:
            logger.warning("  ⚠️ Arduino 개발 환경 온보딩 실패 (계속 진행)")
        else:
            logger.info("  ✅ Arduino 개발 환경 확인 완료")
        
        # 4. USB 시리얼 장치 확인
        logger.info("2. USB 시리얼 장치 확인 중...")
        logger.info("  Arduino Nano를 USB 케이블로 Xavier에 연결해주세요.")
        
        devices = _check_usb_serial_devices_on_xavier(controller)
        
        if devices:
            logger.info("  ✅ USB 시리얼 장치가 감지되었습니다:")
            for device in devices:
                if device.get("path"):
                    logger.info("    - %s", device["path"])
                if device.get("info"):
                    logger.info("    - %s", device["info"])
        else:
            logger.warning("  ⚠️ USB 시리얼 장치가 감지되지 않았습니다.")
            logger.info("  다음을 확인하세요:")
            logger.info("    1. Arduino Nano가 USB 케이블로 연결되어 있는지")
            logger.info("    2. USB 케이블이 데이터 전송을 지원하는지")
            logger.info("    3. Arduino Nano의 전원 LED가 켜져 있는지")
        
        # 5. 최종 안내
        logger.info("=" * 60)
        logger.info("✅ Arduino Nano Wired 개발 환경 설정 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. VSCode에서 Remote-SSH로 Xavier 연결: pk@%s", xavier_ip)
        logger.info("2. PlatformIO 확장 설치")
        logger.info("3. 프로젝트 디렉토리 열기: ~/arduino_projects")
        logger.info("4. PlatformIO 프로젝트 생성:")
        logger.info("   python3 -m platformio project init --board nanoatmega328")
        logger.info("5. 코드 작성 및 업로드")
        logger.info("")
        logger.info("참고:")
        logger.info("- USB 시리얼 장치 접근을 위해 재로그인 또는 재부팅이 필요할 수 있습니다.")
        logger.info("- 시리얼 포트는 /dev/ttyUSB0 또는 /dev/ttyACM0 일 수 있습니다.")
        logger.info("- platformio.ini에서 upload_port와 monitor_port를 지정할 수 있습니다.")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error("Arduino Nano Wired 개발 환경 설정 중 예외 발생: %s", e, exc_info=True)
        return False



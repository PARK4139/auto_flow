"""
Wi-Fi↔UART bridge 기반 wireless 프로그래밍 개발 환경 구축
Arduino Nano + ESP8266 + esp-link를 사용한 무선 프로그래밍 환경 설정

중요: 초기 설정 시 target과의 유선 연결이 필요합니다.
"""
import logging
import textwrap
from pathlib import Path
from typing import Optional, List, Dict

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
    PkWirelessTargetController,
    SetupOpsForPkWirelessTargetController,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def _get_wireless_programming_guide() -> str:
    """wireless 프로그래밍 개발 환경 설정 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    Wi-Fi↔UART bridge 기반 Wireless 프로그래밍 개발 환경 구축 가이드
    ========================================
    
    ## ⚠️ 중요: 초기 의존성 - 유선 연결 필요
    
    **초기 설정 단계에서는 target과의 유선 연결이 필수입니다:**
    
    1. **ESP8266 펌웨어 플래시**: esp-link 펌웨어를 ESP8266에 업로드하려면 USB 케이블이 필요
    2. **초기 Wi-Fi 설정**: esp-link의 AP 모드 접속 및 Wi-Fi 설정
    3. **네트워크 구성 확인**: ESP8266의 IP 주소 확인 및 연결 테스트
    
    **설정 완료 후**: 무선으로 프로그래밍 및 제어 가능
    
    ## 연결 구조
    
    ```
    Xavier
      ↓ [Wi-Fi]
    ESP8266 (esp-link)
      ↓ [UART]
    Arduino Nano (ATmega328P)
    ```
    
    ## 1단계: 초기 설정 (유선 연결 필요)
    
    ### 1.1 ESP8266에 esp-link 펌웨어 플래시 (USB 케이블 필요)
    
    #### 하드웨어 준비:
    1. ESP8266 모듈 (예: ESP-01, NodeMCU, Wemos D1 Mini)
    2. USB-to-Serial 어댑터 (CH340, CP2102 등)
    3. USB 케이블
    
    #### 펌웨어 다운로드:
    ```bash
    # esp-link GitHub에서 펌웨어 다운로드
    # https://github.com/jeelabs/esp-link/releases
    # 최신 버전의 .bin 파일 다운로드
    ```
    
    #### 펌웨어 플래시:
    ```bash
    # esptool 사용 (Xavier에 설치 필요)
    pip3 install esptool
    
    # 펌웨어 플래시
    esptool.py --port /dev/ttyUSB0 write_flash -fs 4MB -fm dout 0x00000 esp-link-v3.2.47.bin
    
    # 또는 Arduino IDE 사용
    # 1. Arduino IDE에서 ESP8266 보드 지원 설치
    # 2. File > Examples > ESP8266 > ESP8266HTTPUpdateServer 참고
    # 3. esp-link 소스 코드 컴파일 및 업로드
    ```
    
    ### 1.2 esp-link 초기 설정 (유선 또는 AP 모드)
    
    #### 방법 1: AP 모드로 접속 (무선, 초기 설정용)
    1. ESP8266 전원 공급
    2. Wi-Fi 네트워크 목록에서 "ESP_xxxxxx" 찾기
    3. 연결 (비밀번호 없음)
    4. 웹 브라우저에서 192.168.4.1 접속
    
    #### 방법 2: USB 케이블로 시리얼 연결 (유선)
    ```bash
    # 시리얼 모니터로 접속
    screen /dev/ttyUSB0 115200
    
    # 또는 minicom
    minicom -D /dev/ttyUSB0 -b 115200
    ```
    
    ### 1.3 Wi-Fi 설정
    
    esp-link 웹 인터페이스에서:
    1. **Wi-Fi 설정**:
       - SSID: 연결할 Wi-Fi 네트워크
       - Password: Wi-Fi 비밀번호
       - Save 후 재부팅
    
    2. **UART 설정**:
       - Baud rate: 115200 (Arduino Nano와 통신)
       - Flow control: None 또는 RTS/CTS
       - Save
    
    3. **고급 설정** (선택사항):
       - TCP 포트: 23 (기본값, telnet)
       - HTTP 포트: 80 (기본값)
       - MQTT 설정 (필요시)
    
    ### 1.4 ESP8266 IP 주소 확인
    
    ```bash
    # 라우터 관리 페이지에서 확인
    # 또는 nmap으로 스캔
    nmap -sn 192.168.0.0/24 | grep -i esp
    
    # 또는 esp-link 웹 인터페이스에서 확인
    curl http://192.168.4.1/status
    ```
    
    ## 2단계: 하드웨어 연결 (Arduino Nano ↔ ESP8266)
    
    ### 연결 방법:
    ```
    Arduino Nano          ESP8266
    -----------          --------
    TX (Pin 1)    →      RX
    RX (Pin 0)    →      TX
    GND           →      GND
    3.3V          →      VCC (주의: 5V 연결 금지!)
    ```
    
    ### 주의사항:
    - ESP8266은 3.3V 전원 필요 (5V 연결 시 손상 가능)
    - 레벨 시프터 사용 권장 (5V ↔ 3.3V 변환)
    - 또는 Arduino Nano의 3.3V 핀 사용 (전류 제한 확인)
    
    ## 3단계: Wireless 프로그래밍 환경 설정
    
    ### 3.1 PlatformIO 설정
    
    #### platformio.ini 설정:
    ```ini
    [platformio]
    default_envs = nano_esp8266_esplink
    
    [env:nano_esp8266_esplink]
    platform = atmelavr
    board = nanoatmega328
    framework = arduino
    monitor_speed = 115200
    
    ; esp-link를 통한 시리얼 모니터 (TCP)
    ; monitor_port = tcp://<esp8266_ip>:23
    ; monitor_protocol = telnet
    ```
    
    ### 3.2 esp-link를 통한 시리얼 통신
    
    #### TCP/Telnet을 통한 시리얼 모니터:
    ```bash
    # esp-link의 TCP 포트(23)로 접속
    telnet <esp8266_ip> 23
    
    # 또는 netcat 사용
    nc <esp8266_ip> 23
    ```
    
    #### HTTP API를 통한 제어:
    ```bash
    # GPIO 제어
    curl http://<esp8266_ip>/v1/pin/13/1  # GPIO 13 HIGH
    curl http://<esp8266_ip>/v1/pin/13/0  # GPIO 13 LOW
    
    # 상태 확인
    curl http://<esp8266_ip>/status
    ```
    
    ### 3.3 Arduino 스케치 업로드
    
    **⚠️ 중요: esp-link는 OTA(Over-The-Air) 스케치 업로드를 지원하지 않습니다.**
    
    Arduino Nano에 스케치를 업로드하려면:
    1. **초기 업로드**: USB 케이블로 직접 연결하여 업로드
    2. **이후 개발**: 코드 수정 후 USB 케이블로 재업로드
    
    **대안:**
    - Arduino Nano 대신 ESP32 사용 (OTA 지원)
    - 또는 ArduinoOTA 라이브러리 사용 (ESP8266 기반 보드)
    
    ## 4단계: 개발 워크플로우
    
    ### 개발 프로세스:
    1. **코드 작성**: VSCode Remote SSH로 Xavier에 연결하여 개발
    2. **컴파일**: PlatformIO로 컴파일
    3. **업로드**: USB 케이블로 Arduino Nano에 업로드
    4. **디버깅**: esp-link를 통한 시리얼 모니터 (TCP/Telnet)
    5. **제어**: esp-link HTTP API를 통한 GPIO 제어
    
    ### 시리얼 모니터 사용:
    ```bash
    # PlatformIO 시리얼 모니터 (USB 직접 연결)
    python3 -m platformio device monitor
    
    # esp-link를 통한 시리얼 모니터 (TCP)
    telnet <esp8266_ip> 23
    ```
    
    ## 5단계: 문제 해결
    
    ### esp-link 연결 안 됨:
    1. ESP8266과 Xavier가 같은 Wi-Fi 네트워크에 있는지 확인
    2. ESP8266 IP 주소 확인
    3. 방화벽 설정 확인
    4. esp-link 웹 인터페이스 접속 테스트
    
    ### 시리얼 통신 안 됨:
    1. UART 연결 확인 (TX↔RX, GND)
    2. Baud rate 확인 (115200)
    3. Flow control 설정 확인
    4. esp-link UART 설정 확인
    
    ### 업로드 실패:
    1. USB 케이블 연결 확인
    2. 시리얼 포트 확인
    3. 보드 타입 확인 (platformio.ini)
    
    ## 요약: 초기 의존성
    
    ✅ **초기 설정 시 유선 연결 필요:**
    - ESP8266 펌웨어 플래시 (USB 케이블)
    - esp-link 초기 설정 (AP 모드 또는 USB 시리얼)
    - Arduino Nano 초기 스케치 업로드 (USB 케이블)
    
    ✅ **설정 완료 후 무선 가능:**
    - 시리얼 모니터 (TCP/Telnet)
    - HTTP API를 통한 GPIO 제어
    - MQTT 통신
    
    ❌ **무선 불가능:**
    - Arduino Nano 스케치 OTA 업로드 (esp-link는 지원하지 않음)
    
    ========================================
    """)


def _check_esp_link_connection(controller: PkWirelessTargetController, esp8266_ip: Optional[str] = None) -> bool:
    """esp-link 연결 확인"""
    if not esp8266_ip:
        logger.warning("ESP8266 IP 주소가 제공되지 않았습니다.")
        return False
    
    logger.info("esp-link 연결 확인 중... (IP: %s)", esp8266_ip)
    
    # 1. Ping 테스트
    logger.info("1. Ping 테스트 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd=f"ping -c 3 {esp8266_ip}",
        timeout_seconds=10,
        use_sudo=False,
    )
    if exit_code == 0:
        logger.info("  ✅ ESP8266에 ping 성공")
    else:
        logger.warning("  ⚠️ ESP8266에 ping 실패")
        return False
    
    # 2. HTTP 상태 확인
    logger.info("2. esp-link HTTP 상태 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd=f"curl -s -m 5 http://{esp8266_ip}/status || echo 'HTTP 요청 실패'",
        timeout_seconds=10,
        use_sudo=False,
    )
    if stdout:
        for line in stdout:
            if "HTTP 요청 실패" not in line:
                logger.info("  ✅ esp-link HTTP 응답: %s", line.strip()[:100])
                return True
            else:
                logger.warning("  ⚠️ esp-link HTTP 요청 실패")
    
    return False


def ensure_arduino_wireless_programming_dev_env_setup(
    xavier_ip: Optional[str] = None,
    xavier_user: Optional[str] = None,
    xavier_pw: Optional[str] = None,
    esp8266_ip: Optional[str] = None,
    skip_initial_wired_setup: bool = False,
) -> bool:
    """
    Wi-Fi↔UART bridge 기반 wireless 프로그래밍 개발 환경을 구축합니다.
    
    ⚠️ 중요: 초기 설정 시 target과의 유선 연결이 필요합니다.
    - ESP8266 펌웨어 플래시 (USB 케이블)
    - esp-link 초기 설정
    - Arduino Nano 초기 스케치 업로드 (USB 케이블)
    
    설정 완료 후에는 무선으로 시리얼 모니터 및 제어가 가능합니다.
    
    Args:
        xavier_ip: Xavier IP 주소. None이면 환경변수 또는 입력받기
        xavier_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        xavier_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        esp8266_ip: ESP8266 IP 주소. None이면 자동 검색 또는 입력받기
        skip_initial_wired_setup: 초기 유선 설정을 건너뛸지 여부
        
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
        logger.info("Wi-Fi↔UART bridge 기반 Wireless 프로그래밍 개발 환경 구축")
        logger.info("=" * 60)
        logger.info("")
        logger.info("⚠️ 중요: 초기 설정 시 target과의 유선 연결이 필요합니다!")
        logger.info("  - ESP8266 펌웨어 플래시: USB 케이블 필요")
        logger.info("  - esp-link 초기 설정: AP 모드 또는 USB 시리얼")
        logger.info("  - Arduino Nano 초기 업로드: USB 케이블 필요")
        logger.info("")
        logger.info("설정 완료 후: 무선으로 시리얼 모니터 및 제어 가능")
        logger.info("=" * 60)
        
        # 가이드 표시
        logger.info(_get_wireless_programming_guide())
        
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
        
        # 3. Arduino 개발 환경 온보딩
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
        
        # 4. 초기 유선 설정 안내 (건너뛰지 않는 경우)
        if not skip_initial_wired_setup:
            logger.info("2. 초기 유선 설정 안내...")
            logger.info("  다음 단계를 수행하세요:")
            logger.info("  a) ESP8266에 esp-link 펌웨어 플래시 (USB 케이블 필요)")
            logger.info("  b) esp-link 초기 설정 (AP 모드 또는 USB 시리얼)")
            logger.info("  c) Wi-Fi 설정 및 ESP8266 IP 주소 확인")
            logger.info("  d) Arduino Nano와 ESP8266 하드웨어 연결")
            logger.info("  e) Arduino Nano 초기 스케치 업로드 (USB 케이블 필요)")
            logger.info("")
            logger.info(get_text_yellow("초기 유선 설정을 완료하셨나요?"))
            
            response = input("continue:y/n").strip().lower()
            if response != 'y':
                logger.info("초기 유선 설정을 완료한 후 다시 실행하세요.")
                return False
        
        # 5. ESP8266 IP 주소 확인
        logger.info("3. ESP8266 IP 주소 확인 중...")
        if not esp8266_ip:
            esp8266_ip = ensure_env_var_completed_2025_11_24(
                "ESP8266_IP",
                func_n=func_n,
                guide_text="ESP8266의 IP 주소를 입력하세요 (예: 192.168.0.100):",
            )
        
        if not esp8266_ip:
            logger.warning("ESP8266 IP 주소가 입력되지 않았습니다.")
            logger.info("ESP8266 IP 주소를 확인하는 방법:")
            logger.info("  1. 라우터 관리 페이지에서 확인")
            logger.info("  2. nmap으로 스캔: nmap -sn 192.168.0.0/24")
            logger.info("  3. esp-link AP 모드에서 확인: http://192.168.4.1")
            return False
        
        # 6. esp-link 연결 확인
        logger.info("4. esp-link 연결 확인 중...")
        if _check_esp_link_connection(controller, esp8266_ip):
            logger.info("  ✅ esp-link 연결 확인됨")
        else:
            logger.warning("  ⚠️ esp-link 연결 확인 실패")
            logger.info("  다음을 확인하세요:")
            logger.info("    - ESP8266과 Xavier가 같은 Wi-Fi 네트워크에 있는지")
            logger.info("    - ESP8266 IP 주소가 올바른지")
            logger.info("    - esp-link가 정상 작동하는지")
            return False
        
        # 7. PlatformIO 설정 안내
        logger.info("5. PlatformIO 설정 안내...")
        logger.info("  platformio.ini에 다음 설정을 추가하세요:")
        logger.info("")
        logger.info("  [env:nano_esp8266_esplink]")
        logger.info("  platform = atmelavr")
        logger.info("  board = nanoatmega328")
        logger.info("  framework = arduino")
        logger.info("  monitor_speed = 115200")
        logger.info("  ; esp-link를 통한 시리얼 모니터 (TCP)")
        logger.info("  ; monitor_port = tcp://%s:23", esp8266_ip)
        logger.info("  ; monitor_protocol = telnet")
        logger.info("")
        
        # 8. 최종 안내
        logger.info("=" * 60)
        logger.info("✅ Wireless 프로그래밍 개발 환경 구축 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. VSCode Remote-SSH로 Xavier 연결: pk@%s", xavier_ip)
        logger.info("2. PlatformIO 확장 설치")
        logger.info("3. 프로젝트 디렉토리 열기: ~/arduino_projects")
        logger.info("4. platformio.ini 설정 (위 참고)")
        logger.info("5. 코드 작성 및 컴파일")
        logger.info("6. USB 케이블로 Arduino Nano에 업로드")
        logger.info("7. esp-link를 통한 시리얼 모니터:")
        logger.info("   telnet %s 23", esp8266_ip)
        logger.info("")
        logger.info("⚠️ 중요:")
        logger.info("- Arduino Nano 스케치 업로드는 USB 케이블이 필요합니다.")
        logger.info("- esp-link는 OTA 업로드를 지원하지 않습니다.")
        logger.info("- 시리얼 모니터는 무선으로 사용 가능합니다 (TCP/Telnet).")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error("Wireless 프로그래밍 개발 환경 구축 중 예외 발생: %s", e, exc_info=True)
        return False







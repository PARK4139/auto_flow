"""
Arduino 개발 환경 설정 (pk_asus - wired - Xavier - wireless - Arduino)
Host Machine에서 wired로 Xavier에 접속하여 Arduino 개발 환경을 설정하고,
Xavier에서 wireless로 Arduino에 연결하는 기능을 제공합니다.
"""
import logging
import textwrap
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_wired_target_controller import PkWiredTargetController
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkModes2,
)

logger = logging.getLogger(__name__)


def _get_arduino_dev_guide() -> str:
    """Arduino 개발 환경 설정 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    Arduino 개발 환경 설정 가이드
    ========================================
    
    ## 연결 구조
    pk_asus (Host Machine) - wired - Xavier - wireless - Arduino
    
    ## 1단계: Host Machine에서 Xavier로 wired 연결
    
    ### 사전 준비:
    1. Host Machine (pk_asus)와 Xavier를 이더넷 케이블로 연결
    2. Xavier의 IP 주소 확인 (기본값: 환경변수 XAVIER_IP)
    3. SSH 연결 테스트:
       ```bash
       ssh pk@<remote_target_ip>
       ```
    
    ### 연결 확인:
    - wired 액션을 통해 Xavier에 접속
    - Xavier의 네트워크 인터페이스 확인:
      ```bash
      ip addr show eth0
      ```
    
    ## 2단계: Xavier에서 Arduino 개발 환경 설정
    
    ### PlatformIO 설치 확인:
    ```bash
    python3 -m platformio --version
    ```
    
    ### 프로젝트 디렉토리:
    ```bash
    cd ~/arduino_projects
    ```
    
    ### USB 시리얼 장치 접근 권한:
    - dialout 그룹에 사용자 추가됨 (재로그인 필요)
    - udev 규칙 설정됨
    
    ## 3단계: Arduino Nano + ESP8266 + esp-link 설정
    
    ### 타겟 구성:
    - **Arduino Nano**: ATmega328P 기반 마이크로컨트롤러
    - **ESP8266**: Wi-Fi 모듈 (esp-link 펌웨어)
    - **esp-link**: Wi-Fi↔UART bridge 펌웨어
    
    ### 하드웨어 연결:
    1. ESP8266에 esp-link 펌웨어 플래시
       - esp-link GitHub: https://github.com/jeelabs/esp-link
       - ESP8266을 USB로 연결하여 펌웨어 업로드
    2. Arduino Nano와 ESP8266 연결:
       - Arduino Nano TX → ESP8266 RX
       - Arduino Nano RX → ESP8266 TX
       - 공통 GND 연결
       - ESP8266 VCC → 3.3V (주의: 5V 연결 금지!)
    
    ### esp-link 설정:
    1. ESP8266의 AP 모드로 접속 (기본 SSID: "ESP_xxxxxx")
    2. 웹 브라우저에서 192.168.4.1 접속
    3. Wi-Fi 설정:
       - SSID: 연결할 Wi-Fi 네트워크
       - Password: Wi-Fi 비밀번호
    4. UART 설정:
       - Baud rate: 115200 (기본값)
       - Flow control: None 또는 RTS/CTS
    5. 저장 후 재부팅
    
    ### esp-link 확인:
    ```bash
    # ESP8266의 IP 주소 확인 (라우터 관리 페이지 또는 nmap)
    nmap -sn 192.168.0.0/24 | grep -i esp
    
    # esp-link 웹 인터페이스 접속
    curl http://<esp8266_ip>/
    
    # esp-link 상태 확인
    curl http://<esp8266_ip>/status
    ```
    
    ### Arduino Nano 코드 예시:
    ```cpp
    // Arduino Nano에서 ESP8266(esp-link)를 통해 Wi-Fi 통신
    #include <SoftwareSerial.h>
    
    // ESP8266과의 통신을 위한 소프트웨어 시리얼
    SoftwareSerial espSerial(2, 3); // RX, TX
    
    void setup() {
      Serial.begin(115200);  // PC와의 시리얼 통신
      espSerial.begin(115200);  // ESP8266과의 통신
      
      // esp-link 초기화 대기
      delay(2000);
    }
    
    void loop() {
      // ESP8266으로 데이터 전송
      if (Serial.available()) {
        espSerial.write(Serial.read());
      }
      
      // ESP8266에서 데이터 수신
      if (espSerial.available()) {
        Serial.write(espSerial.read());
      }
    }
    ```
    
    ### Xavier에서 Arduino 연결 확인:
    ```bash
    # ESP8266 IP 주소로 ping 테스트
    ping <esp8266_ip>
    
    # esp-link를 통한 HTTP 요청
    curl http://<esp8266_ip>/v1/pin/13/1  # GPIO 13 HIGH
    curl http://<esp8266_ip>/v1/pin/13/0  # GPIO 13 LOW
    ```
    
    ## 4단계: VSCode Remote SSH로 개발
    
    ### VSCode 설정:
    1. VSCode에서 Remote-SSH 확장 설치
    2. F1 > 'Remote-SSH: Connect to Host'
    3. 'pk@<remote_target_ip>' 입력
    4. PlatformIO 확장 설치
    5. 프로젝트 디렉토리 열기: ~/arduino_projects
    
    ### PlatformIO 프로젝트 생성:
    ```bash
    cd ~/arduino_projects
    python3 -m platformio project init --board uno
    # 또는 ESP32의 경우
    python3 -m platformio project init --board esp32dev
    ```
    
    ### 코드 업로드:
    - VSCode에서 PlatformIO: Upload 버튼 클릭
    - 또는 CLI: `python3 -m platformio run --target upload`
    
    ## 5단계: Arduino와 통신
    
    ### 시리얼 통신 (USB):
    ```bash
    # 시리얼 포트 확인
    ls /dev/ttyUSB* /dev/ttyACM*
    
    # 시리얼 모니터
    python3 -m platformio device monitor
    ```
    
    ### Wi-Fi 통신:
    - Arduino의 IP 주소로 HTTP 요청
    - REST API 또는 WebSocket 사용
    - MQTT 브로커 사용 가능
    
    ## 문제 해결
    
    ### USB 장치 인식 안 됨:
    1. dialout 그룹 확인: `groups`
    2. 재로그인 또는 재부팅
    3. udev 규칙 확인: `ls -l /etc/udev/rules.d/99-platformio-udev.rules`
    
    ### Wi-Fi 연결 안 됨:
    1. Arduino와 Xavier가 같은 Wi-Fi 네트워크에 있는지 확인
    2. 방화벽 설정 확인
    3. Arduino IP 주소 확인 (시리얼 모니터)
    
    ### PlatformIO 업로드 실패:
    1. 보드 연결 확인
    2. 보드 타입 확인 (platformio.ini)
    3. 드라이버 설치 확인
    
    ========================================
    """)


def ensure_arduino_dev_via_wired_remote_target_wireless_arduino(
        remote_target_ip: Optional[str] = None,
        remote_target_user: Optional[str] = None,
        remote_target_pw: Optional[str] = None,
        arduino_wifi_ssid: Optional[str] = None,
        arduino_wifi_password: Optional[str] = None,
) -> bool:
    """
    Host Machine에서 wired로 Xavier에 접속하여 Arduino 개발 환경을 설정하고,
    Xavier에서 wireless로 Arduino에 연결하는 전체 프로세스를 수행합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        arduino_wifi_ssid: Arduino가 연결할 Wi-Fi SSID (선택사항)
        arduino_wifi_password: Arduino가 연결할 Wi-Fi 비밀번호 (선택사항)
        
    Returns:
        bool: 설정 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.ensure_arduino_dev_environment_onboarded_on_remote_target import (
            ensure_arduino_dev_environment_onboarded_on_remote_target,
        )

        func_n = get_caller_name()

        logger.info("=" * 60)
        logger.info("Arduino 개발 환경 설정 시작")
        logger.info("구조: pk_asus (wired) - Xavier (wireless) - Arduino")
        logger.info("=" * 60)

        # 가이드 표시
        logger.info(_get_arduino_dev_guide())

        # 1. remote_target 연결 정보 가져오기
        if not remote_target_ip:
            remote_target_ip = ensure_env_var_completed("XAVIER_IP")
        if not remote_target_user:
            remote_target_user = ensure_env_var_completed("XAVIER_USER")
        if not remote_target_pw:
            remote_target_pw = ensure_env_var_completed("XAVIER_PW")

        # 2. Host Machine에서 Xavier로 wired 연결 확인
        logger.info("1. Host Machine에서 Xavier로 wired 연결 확인 중...")
        wired_controller = PkWiredTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            
        )

        # 연결 테스트 (SSH를 통해)
        logger.info("  - remote_target 연결 테스트 중...")
        try:
            # wired controller를 통해 SSH 연결 테스트
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # SSH 키 파일 확인
            ssh_key_path = getattr(wired_controller._target, "f_local_ssh_private_key", None)
            if ssh_key_path and Path(ssh_key_path).exists():
                key = paramiko.Ed25519Key(file_name=ssh_key_path)
                ssh.connect(
                    hostname=remote_target_ip,
                    port=getattr(wired_controller._target, "port", 22),
                    username=remote_target_user,
                    pkey=key,
                    timeout=10,
                )
            else:
                # 비밀번호 인증
                ssh.connect(
                    hostname=remote_target_ip,
                    port=getattr(wired_controller._target, "port", 22),
                    username=remote_target_user,
                    password=remote_target_pw,
                    timeout=10,
                )

            stdin, stdout, stderr = ssh.exec_command("echo 'Xavier wired connection test'")
            exit_code = stdout.channel.recv_exit_status()
            ssh.close()

            if exit_code == 0:
                logger.info("  ✅ Xavier wired 연결 확인됨")
            else:
                logger.error("  ❌ Xavier wired 연결 실패")
                logger.error("  이더넷 케이블 연결 및 IP 주소를 확인하세요.")
                return False
        except Exception as e:
            logger.error("  ❌ Xavier wired 연결 실패: %s", e)
            logger.error("  이더넷 케이블 연결 및 IP 주소를 확인하세요.")
            return False

        # 3. Xavier에서 Arduino 개발 환경 온보딩
        logger.info("2. Xavier에서 Arduino 개발 환경 온보딩 중...")
        success = ensure_arduino_dev_environment_onboarded_on_remote_target(
            remote_target_ip=remote_target_ip,
            remote_target_user=remote_target_user,
            remote_target_pw=remote_target_pw,
        )

        if not success:
            logger.error("  ❌ Arduino 개발 환경 온보딩 실패")
            return False

        logger.info("  ✅ Arduino 개발 환경 온보딩 완료")

        # 4. Xavier에서 Arduino로 wireless 연결 설정 (선택사항)
        if arduino_wifi_ssid:
            logger.info("3. Xavier에서 Arduino Wi-Fi 연결 정보 설정 중...")
            logger.info("  Arduino가 연결할 Wi-Fi: %s", arduino_wifi_ssid)
            logger.info("  참고: Arduino 스케치에서 Wi-Fi 설정을 업데이트하세요.")
            logger.info("  예시 코드:")
            logger.info("    const char* ssid = \"%s\";", arduino_wifi_ssid)
            if arduino_wifi_password:
                logger.info("    const char* password = \"%s\";", arduino_wifi_password)

        # 5. 최종 안내
        logger.info("=" * 60)
        logger.info("✅ Arduino 개발 환경 설정 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. VSCode에서 Remote-SSH로 remote_target 연결: pk@%s", remote_target_ip)
        logger.info("2. PlatformIO 확장 설치")
        logger.info("3. 프로젝트 디렉토리 열기: ~/arduino_projects")
        logger.info("4. Arduino 보드 연결 (USB 또는 Wi-Fi)")
        logger.info("5. PlatformIO 프로젝트 생성 및 개발 시작")
        logger.info("")
        logger.info("참고:")
        logger.info("- USB 시리얼 장치 접근을 위해 재로그인 또는 재부팅이 필요할 수 있습니다.")
        logger.info("- Arduino Wi-Fi 연결은 Arduino 스케치에서 설정해야 합니다.")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("Arduino 개발 환경 설정 중 예외 발생: %s", e, exc_info=True)
        return False

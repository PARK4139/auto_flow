"""
Arduino에 OTA uploader agent 설치
유선 연결을 초기 의존으로 하여 OTA 에이전트를 설치합니다.

⚠️ 중요: 초기 설치 시 유선 연결이 필요합니다.
- Arduino Nano는 Wi-Fi가 없으므로 ESP8266을 통해 OTA 구현
- ESP8266에 OTA 에이전트 설치 (ArduinoOTA 라이브러리)
- 또는 ESP8266 기반 보드에 직접 OTA 에이전트 설치
"""
import logging
import textwrap
import tempfile
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
    PkWirelessTargetController,
    SetupOpsForPkWirelessTargetController,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def _get_ota_agent_install_guide() -> str:
    """OTA uploader agent 설치 가이드 텍스트 반환"""
    return textwrap.dedent("""
    ========================================
    OTA Uploader Agent 설치 가이드
    ========================================
    
    ## ⚠️ 중요: 초기 의존성 - 유선 연결 필요
    
    **OTA 에이전트 초기 설치 시 유선 연결이 필수입니다:**
    
    1. **ESP8266에 OTA 에이전트 설치**: USB 케이블로 연결하여 업로드
    2. **Wi-Fi 설정**: OTA 에이전트가 Wi-Fi에 연결되도록 설정
    3. **네트워크 확인**: OTA 서버와 통신 가능한지 확인
    
    **설정 완료 후**: 무선으로 스케치 업로드 가능
    
    ## Arduino Nano + ESP8266 구성에서의 OTA
    
    ### 옵션 1: ESP8266에 OTA 에이전트 설치 (권장)
    
    ESP8266에 ArduinoOTA 라이브러리를 사용한 OTA 에이전트를 설치합니다.
    ESP8266이 Arduino Nano와 UART로 통신하여 업로드를 중계할 수 있습니다.
    
    ### 옵션 2: ESP8266 기반 보드 사용
    
    NodeMCU, Wemos D1 Mini 등 ESP8266 기반 보드를 사용하면
    직접 OTA 업로드가 가능합니다.
    
    ## 1단계: ESP8266에 OTA 에이전트 설치 (유선 연결 필요)
    
    ### 하드웨어 준비:
    1. ESP8266 모듈 또는 ESP8266 기반 보드
    2. USB 케이블
    3. Arduino Nano (옵션 1의 경우)
    
    ### ArduinoOTA 라이브러리 설치:
    ```cpp
    // ESP8266용 OTA 에이전트 스케치 예시
    #include <ESP8266WiFi.h>
    #include <ArduinoOTA.h>
    #include <ESP8266mDNS.h>
    
    const char* ssid = "YOUR_WIFI_SSID";
    const char* password = "YOUR_WIFI_PASSWORD";
    
    void setup() {
      Serial.begin(115200);
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid, password);
      
      while (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.println("Wi-Fi 연결 실패, 재시도 중...");
        delay(5000);
      }
      
      // OTA 설정
      ArduinoOTA.setHostname("arduino-ota");
      ArduinoOTA.setPassword("ota_password");  // 선택사항
      
      ArduinoOTA.onStart([]() {
        Serial.println("OTA 업로드 시작");
      });
      
      ArduinoOTA.onEnd([]() {
        Serial.println("\\nOTA 업로드 완료");
      });
      
      ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
        Serial.printf("진행률: %u%%\\r", (progress / (total / 100)));
      });
      
      ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("OTA 오류[%u]: ", error);
        if (error == OTA_AUTH_ERROR) Serial.println("인증 실패");
        else if (error == OTA_BEGIN_ERROR) Serial.println("시작 실패");
        else if (error == OTA_CONNECT_ERROR) Serial.println("연결 실패");
        else if (error == OTA_RECEIVE_ERROR) Serial.println("수신 실패");
        else if (error == OTA_END_ERROR) Serial.println("종료 실패");
      });
      
      ArduinoOTA.begin();
      Serial.println("OTA 준비 완료");
      Serial.print("IP 주소: ");
      Serial.println(WiFi.localIP());
    }
    
    void loop() {
      ArduinoOTA.handle();
      // 다른 작업...
    }
    ```
    
    ### 업로드 방법:
    1. Arduino IDE 또는 PlatformIO 사용
    2. USB 케이블로 ESP8266에 업로드
    3. 시리얼 모니터에서 IP 주소 확인
    
    ## 2단계: OTA 업로드 테스트
    
    ### PlatformIO에서 OTA 업로드:
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
    python3 -m platformio run --target upload
    ```
    
    ## 3단계: Xavier에서 OTA 업로드
    
    ### OTA 업로드 스크립트:
    ```bash
    # PlatformIO OTA 업로드
    python3 -m platformio run --target upload --upload-port <esp8266_ip>
    ```
    
    ## 문제 해결
    
    ### OTA 업로드 실패:
    1. ESP8266과 Xavier가 같은 Wi-Fi 네트워크에 있는지 확인
    2. ESP8266 IP 주소 확인
    3. 방화벽 설정 확인
    4. OTA 비밀번호 확인 (설정한 경우)
    
    ### 연결 안 됨:
    1. ESP8266이 Wi-Fi에 연결되어 있는지 확인
    2. 시리얼 모니터에서 IP 주소 확인
    3. ping 테스트: `ping <esp8266_ip>`
    
    ========================================
    """)


def _generate_ota_agent_sketch(wifi_ssid: str, wifi_password: str, ota_password: Optional[str] = None) -> str:
    """OTA 에이전트 스케치 코드 생성"""
    ota_auth = f'  ArduinoOTA.setPassword("{ota_password}");' if ota_password else "  // ArduinoOTA.setPassword(\"ota_password\");  // 비밀번호 설정 (선택사항)"
    
    return textwrap.dedent(f"""
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>
#include <ESP8266mDNS.h>

const char* ssid = "{wifi_ssid}";
const char* password = "{wifi_password}";

void setup() {{
  Serial.begin(115200);
  Serial.println("OTA 에이전트 시작");
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  Serial.print("Wi-Fi 연결 중");
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {{
    Serial.print(".");
    delay(500);
  }}
  Serial.println();
  Serial.println("Wi-Fi 연결 성공");
  
  // OTA 설정
  ArduinoOTA.setHostname("arduino-ota");
{ota_auth}
  
  ArduinoOTA.onStart([]() {{
    Serial.println("OTA 업로드 시작");
  }});
  
  ArduinoOTA.onEnd([]() {{
    Serial.println("\\nOTA 업로드 완료");
  }});
  
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {{
    Serial.printf("진행률: %u%%\\r", (progress / (total / 100)));
  }});
  
  ArduinoOTA.onError([](ota_error_t error) {{
    Serial.printf("OTA 오류[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("인증 실패");
    else if (error == OTA_BEGIN_ERROR) Serial.println("시작 실패");
    else if (error == OTA_CONNECT_ERROR) Serial.println("연결 실패");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("수신 실패");
    else if (error == OTA_END_ERROR) Serial.println("종료 실패");
  }});
  
  ArduinoOTA.begin();
  Serial.println("OTA 준비 완료");
  Serial.print("IP 주소: ");
  Serial.println(WiFi.localIP());
  Serial.print("호스트명: arduino-ota.local");
}}

void loop() {{
  ArduinoOTA.handle();
  delay(10);
}}
""")


def ensure_ota_uploader_agent_installed_on_arduino(
    xavier_ip: Optional[str] = None,
    xavier_user: Optional[str] = None,
    xavier_pw: Optional[str] = None,
    wifi_ssid: Optional[str] = None,
    wifi_password: Optional[str] = None,
    ota_password: Optional[str] = None,
    serial_port: Optional[str] = None,
) -> bool:
    """
    Arduino에 OTA uploader agent를 설치합니다.
    
    ⚠️ 중요: 초기 설치 시 유선 연결이 필요합니다.
    - ESP8266에 OTA 에이전트 스케치 업로드 (USB 케이블)
    - Wi-Fi 설정 및 OTA 설정
    
    설정 완료 후에는 무선으로 스케치 업로드가 가능합니다.
    
    Args:
        xavier_ip: Xavier IP 주소. None이면 환경변수 또는 입력받기
        xavier_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        xavier_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        wifi_ssid: Wi-Fi SSID. None이면 입력받기
        wifi_password: Wi-Fi 비밀번호. None이면 입력받기
        ota_password: OTA 업로드 비밀번호 (선택사항). None이면 입력받기
        serial_port: 시리얼 포트 (예: /dev/ttyUSB0). None이면 자동 감지
        
    Returns:
        bool: 설치 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
        
        func_n = get_caller_name()
        
        logger.info("=" * 60)
        logger.info("OTA Uploader Agent 설치 시작")
        logger.info("=" * 60)
        logger.info("")
        logger.info("⚠️ 중요: 초기 설치 시 유선 연결이 필요합니다!")
        logger.info("  - ESP8266을 USB 케이블로 Xavier에 연결")
        logger.info("  - OTA 에이전트 스케치 업로드")
        logger.info("")
        logger.info("설정 완료 후: 무선으로 스케치 업로드 가능")
        logger.info("=" * 60)
        
        # 가이드 표시
        logger.info(_get_ota_agent_install_guide())
        
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
        
        # 3. Wi-Fi 설정 입력받기
        logger.info("1. Wi-Fi 설정 입력 중...")
        if not wifi_ssid:
            wifi_ssid = ensure_env_var_completed_2025_11_24(
                "WIFI_SSID",
                func_n=func_n,
                guide_text="ESP8266이 연결할 Wi-Fi SSID를 입력하세요:",
            )
        if not wifi_password:
            wifi_password = ensure_env_var_completed_2025_11_24(
                "WIFI_PASSWORD",
                func_n=func_n,
                guide_text="Wi-Fi 비밀번호를 입력하세요:",
            )
        if not ota_password:
            ota_password_input = ensure_env_var_completed_2025_11_24(
                "OTA_PASSWORD",
                func_n=func_n,
                guide_text="OTA 업로드 비밀번호를 입력하세요 (선택사항, Enter로 건너뛰기):",
            )
            ota_password = ota_password_input if ota_password_input else None
        
        # 4. 시리얼 포트 확인
        logger.info("2. 시리얼 포트 확인 중...")
        logger.info("  ESP8266을 USB 케이블로 Xavier에 연결해주세요.")
        
        if not serial_port:
            # 시리얼 포트 자동 감지
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd="ls -1 /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -1 || echo ''",
                timeout_seconds=10,
                use_sudo=False,
            )
            if stdout and stdout[0].strip():
                serial_port = stdout[0].strip()
                logger.info("  ✅ 시리얼 포트 자동 감지: %s", serial_port)
            else:
                serial_port = ensure_env_var_completed_2025_11_24(
                    "SERIAL_PORT",
                    func_n=func_n,
                    guide_text="ESP8266의 시리얼 포트를 입력하세요 (예: /dev/ttyUSB0):",
                )
        
        if not serial_port:
            logger.error("시리얼 포트가 입력되지 않았습니다.")
            return False
        
        # 5. OTA 에이전트 스케치 생성
        logger.info("3. OTA 에이전트 스케치 생성 중...")
        ota_sketch = _generate_ota_agent_sketch(wifi_ssid, wifi_password, ota_password)
        
        # 임시 스케치 파일 생성
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ino', encoding='utf-8') as temp_f:
            temp_sketch_path = temp_f.name
            temp_f.write(ota_sketch)
        
        try:
            # Xavier에 스케치 전송
            remote_sketch_path = f"~/arduino_projects/ota_agent/ota_agent.ino"
            logger.info("  OTA 에이전트 스케치를 Xavier에 전송 중...")
            ok = controller.ensure_file_transferred_to_target(
                temp_sketch_path,
                remote_sketch_path,
            )
            
            if not ok:
                logger.error("스케치 전송 실패")
                return False
            
            # 6. PlatformIO 프로젝트 생성 및 업로드 안내
            logger.info("4. PlatformIO 프로젝트 생성 안내...")
            logger.info("  Xavier에서 다음 명령을 실행하세요:")
            logger.info("")
            logger.info("  cd ~/arduino_projects")
            logger.info("  python3 -m platformio project init --board nodemcuv2 --project-dir ota_agent")
            logger.info("  cp ota_agent.ino src/main.cpp")
            logger.info("")
            logger.info("  # platformio.ini 설정:")
            logger.info("  # upload_port = %s", serial_port)
            logger.info("")
            logger.info("  python3 -m platformio run --target upload")
            logger.info("")
            
            # 7. 업로드 확인
            logger.info("5. OTA 에이전트 업로드 확인...")
            logger.info("  시리얼 모니터에서 다음을 확인하세요:")
            logger.info("    - Wi-Fi 연결 성공")
            logger.info("    - IP 주소 출력")
            logger.info("    - 'OTA 준비 완료' 메시지")
            logger.info("")
            logger.info("  시리얼 모니터 실행:")
            logger.info("    python3 -m platformio device monitor --port %s", serial_port)
            
            # 8. 최종 안내
            logger.info("=" * 60)
            logger.info("✅ OTA Uploader Agent 설치 가이드 완료")
            logger.info("=" * 60)
            logger.info("")
            logger.info("다음 단계:")
            logger.info("1. 위의 명령을 실행하여 OTA 에이전트를 ESP8266에 업로드")
            logger.info("2. 시리얼 모니터에서 ESP8266 IP 주소 확인")
            logger.info("3. 이후 무선으로 스케치 업로드 가능:")
            logger.info("   python3 -m platformio run --target upload --upload-port <esp8266_ip>")
            logger.info("")
            logger.info("⚠️ 참고:")
            logger.info("- 초기 설치 시 유선 연결이 필요합니다.")
            logger.info("- 설치 완료 후에는 무선으로 업로드 가능합니다.")
            logger.info("=" * 60)
            
            return True
            
        finally:
            import os
            if os.path.exists(temp_sketch_path):
                try:
                    os.remove(temp_sketch_path)
                except Exception:
                    pass
        
    except Exception as e:
        logger.error("OTA Uploader Agent 설치 중 예외 발생: %s", e, exc_info=True)
        return False



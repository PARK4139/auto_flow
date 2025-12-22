"""
Xavier에 Arduino OTA 개발 환경 설정
OTA(Over-The-Air) 업로드를 위한 개발 환경을 구축합니다.
"""
import logging
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def _get_ota_development_environment_guide() -> str:
    """OTA 개발 환경 설정 가이드 텍스트 반환 (파일에서 읽어옴)"""
    guide_file = D_PK_EXTERNAL_TOOLS / "arduino_ota_development_environment_guide.txt"
    guide_text = get_str_from_f(f=str(guide_file))
    
    if not guide_text:
        logger.warning("가이드 파일을 읽을 수 없습니다: %s", guide_file)
        return "가이드 파일을 읽을 수 없습니다."
    
    return guide_text


def ensure_arduino_ota_development_environment_on_remote_target(
    remote_target_ip: Optional[str] = None,
    remote_target_user: Optional[str] = None,
    remote_target_pw: Optional[str] = None,
    esp8266_ip: Optional[str] = None,
    esp32_ip: Optional[str] = None,
    ota_password: Optional[str] = None,
) -> bool:
    """
    Xavier에 Arduino OTA 개발 환경을 설정합니다.
    
    OTA(Over-The-Air) 업로드를 위한 PlatformIO 설정 및 워크플로우를 구축합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        esp8266_ip: ESP8266 IP 주소 (선택사항). None이면 입력받기
        esp32_ip: ESP32 IP 주소 (선택사항). None이면 입력받기
        ota_password: OTA 업로드 비밀번호 (선택사항). None이면 입력받기
        
    Returns:
        bool: 설정 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        
        func_n = get_caller_name()
        
        logger.info("=" * 60)
        logger.info("Arduino OTA 개발 환경 설정 시작")
        logger.info("=" * 60)
        
        # 가이드 표시
        logger.info(_get_ota_development_environment_guide())
        
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
        
        # 3. PlatformIO 설치 확인
        logger.info("1. PlatformIO 설치 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd="python3 -m platformio --version",
            timeout_seconds=30,
            use_sudo=False,
        )
        
        if exit_code == 0 and stdout:
            pio_version = stdout[0].strip() if stdout else "unknown"
            logger.info("  ✅ PlatformIO 버전: %s", pio_version)
        else:
            logger.warning("  ⚠️ PlatformIO가 설치되어 있지 않습니다.")
            logger.info("  'onboard Arduino dev environment on Xavier' 작업을 먼저 실행하세요.")
            return False
        
        # 4. OTA 프로젝트 디렉토리 생성
        logger.info("2. OTA 프로젝트 디렉토리 생성 중...")
        ota_project_dir = "~/arduino_projects/ota_examples"
        create_dir_cmd = f"mkdir -p {ota_project_dir}"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=create_dir_cmd,
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0:
            logger.info("  ✅ OTA 프로젝트 디렉토리 생성 완료: %s", ota_project_dir)
        else:
            logger.warning("  ⚠️ 디렉토리 생성 실패")
        
        # 5. OTA platformio.ini 템플릿 생성
        logger.info("3. OTA platformio.ini 템플릿 생성 중...")
        
        # ESP8266 IP 주소 확인
        if not esp8266_ip:
            esp8266_ip_input = ensure_env_var_completed(
                "ESP8266_IP",
                func_n=func_n,
                guide_text="ESP8266 IP 주소를 입력하세요 (선택사항, Enter로 건너뛰기):",
            )
            esp8266_ip = esp8266_ip_input if esp8266_ip_input else None
        
        # ESP32 IP 주소 확인
        if not esp32_ip:
            esp32_ip_input = ensure_env_var_completed(
                "ESP32_IP",
                func_n=func_n,
                guide_text="ESP32 IP 주소를 입력하세요 (선택사항, Enter로 건너뛰기):",
            )
            esp32_ip = esp32_ip_input if esp32_ip_input else None
        
        # OTA 비밀번호 확인
        if not ota_password:
            ota_password_input = ensure_env_var_completed(
                "OTA_PASSWORD",
                func_n=func_n,
                guide_text="OTA 업로드 비밀번호를 입력하세요 (선택사항, Enter로 건너뛰기):",
            )
            ota_password = ota_password_input if ota_password_input else None
        
        # platformio.ini 템플릿 생성
        platformio_ini_content = """[platformio]
default_envs = nodemcuv2

# ESP8266 NodeMCU v2 OTA 설정
[env:nodemcuv2]
platform = espressif8266
board = nodemcuv2
framework = arduino
upload_protocol = espota
"""
        
        if esp8266_ip:
            platformio_ini_content += f"upload_port = {esp8266_ip}\n"
        else:
            platformio_ini_content += "# upload_port = <esp8266_ip>  # ESP8266 IP 주소 입력 필요\n"
        
        if ota_password:
            platformio_ini_content += f"upload_flags = --auth={ota_password}\n"
        else:
            platformio_ini_content += "# upload_flags = --auth=ota_password  # OTA 비밀번호 설정 (선택사항)\n"
        
        platformio_ini_content += """monitor_speed = 115200

# ESP32 Dev Module OTA 설정
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
upload_protocol = espota
"""
        
        if esp32_ip:
            platformio_ini_content += f"upload_port = {esp32_ip}\n"
        else:
            platformio_ini_content += "# upload_port = <esp32_ip>  # ESP32 IP 주소 입력 필요\n"
        
        if ota_password:
            platformio_ini_content += f"upload_flags = --auth={ota_password}\n"
        else:
            platformio_ini_content += "# upload_flags = --auth=ota_password  # OTA 비밀번호 설정 (선택사항)\n"
        
        platformio_ini_content += """monitor_speed = 115200
"""
        
        # platformio.ini 템플릿 파일 생성
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".ini",
            encoding="utf-8",
        ) as temp_f:
            temp_ini_path = temp_f.name
            temp_f.write(platformio_ini_content)
        
        try:
            # Xavier에 platformio.ini 템플릿 전송
            remote_ini_path = f"{ota_project_dir}/platformio.ini.ota_template"
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_ini_path,
                remote_ini_path,
            )
            
            if ok:
                logger.info("  ✅ OTA platformio.ini 템플릿 생성 완료: %s", remote_ini_path)
            else:
                logger.warning("  ⚠️ platformio.ini 템플릿 생성 실패")
        finally:
            import os
            if temp_ini_path and os.path.exists(temp_ini_path):
                try:
                    os.remove(temp_ini_path)
                except Exception as e:
                    pass
        
        # 6. OTA 에이전트 스케치 템플릿 생성
        logger.info("4. OTA 에이전트 스케치 템플릿 생성 중...")
        
        ota_agent_sketch = """#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* ota_password = "ota_password";  // OTA 업로드 비밀번호

void setup() {
  Serial.begin(115200);
  Serial.println("OTA 에이전트 시작");
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  Serial.print("Wi-Fi 연결 중");
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.println("Wi-Fi 연결 성공");
  
  // OTA 설정
  ArduinoOTA.setHostname("arduino-ota");
  ArduinoOTA.setPassword(ota_password);
  
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
  Serial.print("호스트명: arduino-ota.local");
}

void loop() {
  ArduinoOTA.handle();
  delay(10);
}
"""
        
        # OTA 에이전트 스케치 파일 생성
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".cpp",
            encoding="utf-8",
        ) as temp_f:
            temp_sketch_path = temp_f.name
            temp_f.write(ota_agent_sketch)
        
        try:
            # Xavier에 OTA 에이전트 스케치 전송
            remote_sketch_path = f"{ota_project_dir}/ota_agent.cpp.template"
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_sketch_path,
                remote_sketch_path,
            )
            
            if ok:
                logger.info("  ✅ OTA 에이전트 스케치 템플릿 생성 완료: %s", remote_sketch_path)
            else:
                logger.warning("  ⚠️ OTA 에이전트 스케치 템플릿 생성 실패")
        finally:
            import os
            if temp_sketch_path and os.path.exists(temp_sketch_path):
                try:
                    os.remove(temp_sketch_path)
                except Exception as e:
                    pass
        
        # 7. OTA 업로드 스크립트 생성
        logger.info("5. OTA 업로드 스크립트 생성 중...")
        
        ota_upload_script = """#!/bin/bash
# OTA 업로드 스크립트
# 사용법: ./ota_upload.sh <esp8266_ip> [ota_password]

ESP8266_IP="${1:-192.168.0.100}"
OTA_PASSWORD="${2:-ota_password}"

echo "OTA 업로드 시작..."
echo "ESP8266 IP: $ESP8266_IP"
echo "OTA 비밀번호: $OTA_PASSWORD"

# 컴파일 및 OTA 업로드
python3 -m platformio run --target upload --upload-port "$ESP8266_IP" --upload-flags "--auth=$OTA_PASSWORD"

if [ $? -eq 0 ]; then
    echo "✅ OTA 업로드 성공"
else
    echo "❌ OTA 업로드 실패"
    exit 1
fi
"""
        
        # OTA 업로드 스크립트 파일 생성
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".sh",
            encoding="utf-8",
        ) as temp_f:
            temp_script_path = temp_f.name
            temp_f.write(ota_upload_script)
        
        try:
            # Xavier에 OTA 업로드 스크립트 전송
            remote_script_path = f"{ota_project_dir}/ota_upload.sh"
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_script_path,
                remote_script_path,
            )
            
            if ok:
                # 실행 권한 부여
                chmod_cmd = f"chmod +x {remote_script_path}"
                controller.ensure_command_to_remote_target(
                    cmd=chmod_cmd,
                    timeout_seconds=10,
                    use_sudo=False,
                )
                logger.info("  ✅ OTA 업로드 스크립트 생성 완료: %s", remote_script_path)
            else:
                logger.warning("  ⚠️ OTA 업로드 스크립트 생성 실패")
        finally:
            import os
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception as e:
                    pass
        
        # 8. 최종 안내
        logger.info("=" * 60)
        logger.info("✅ Arduino OTA 개발 환경 설정 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("생성된 파일:")
        logger.info("  - %s/platformio.ini.ota_template", ota_project_dir)
        logger.info("  - %s/ota_agent.cpp.template", ota_project_dir)
        logger.info("  - %s/ota_upload.sh", ota_project_dir)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. OTA 에이전트 설치:")
        logger.info("   - 'install OTA uploader agent on Arduino' 작업 실행 (wired 액션)")
        logger.info("   - 또는 템플릿 파일을 참고하여 직접 업로드")
        logger.info("")
        logger.info("2. OTA 프로젝트 생성:")
        logger.info("   cd %s", ota_project_dir)
        logger.info("   python3 -m platformio project init --board nodemcuv2 --project-dir my_ota_project")
        logger.info("   cp platformio.ini.ota_template my_ota_project/platformio.ini")
        logger.info("   # platformio.ini에서 IP 주소 및 비밀번호 수정")
        logger.info("")
        logger.info("3. OTA 업로드:")
        logger.info("   cd my_ota_project")
        logger.info("   python3 -m platformio run --target upload")
        logger.info("   # 또는 스크립트 사용: ../ota_upload.sh <esp8266_ip> [ota_password]")
        logger.info("")
        logger.info("⚠️ 참고:")
        logger.info("- 초기 OTA 에이전트 설치 시 USB 케이블이 필요합니다.")
        logger.info("- OTA 업로드는 Wi-Fi 연결이 안정적이어야 합니다.")
        logger.info("- OTA 비밀번호 설정을 권장합니다 (보안).")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error("Arduino OTA 개발 환경 설정 중 예외 발생: %s", e, exc_info=True)
        return False



"""
Arduino 타겟 구성 정의 클래스
확장 가능한 구조로 다양한 Arduino 타겟을 지원합니다.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class ArduinoTargetType(Enum):
    """Arduino 타겟 타입"""
    NANO_ESP8266_ESPLINK = "nano_esp8266_esplink"  # Arduino Nano + ESP8266 + esp-link
    NANO_STANDALONE = "nano_standalone"  # Arduino Nano 단독
    UNO = "uno"  # Arduino Uno
    ESP32_DEV = "esp32dev"  # ESP32 Dev Board
    NANO_ESP32 = "nano_esp32"  # Arduino Nano ESP32


@dataclass
class ArduinoTargetConfig:
    """Arduino 타겟 구성 정보"""
    target_type: ArduinoTargetType
    board_name: str
    platform: str
    framework: str
    monitor_speed: int = 115200
    description: str = ""
    hardware_components: List[str] = None
    connection_guide: str = ""
    platformio_env: str = ""
    
    def __post_init__(self):
        if self.hardware_components is None:
            self.hardware_components = []
        if not self.platformio_env:
            self.platformio_env = self.target_type.value


# 타겟 구성 정의
ARDUINO_TARGET_CONFIGS: Dict[ArduinoTargetType, ArduinoTargetConfig] = {
    ArduinoTargetType.NANO_ESP8266_ESPLINK: ArduinoTargetConfig(
        target_type=ArduinoTargetType.NANO_ESP8266_ESPLINK,
        board_name="nanoatmega328",
        platform="atmelavr",
        framework="arduino",
        monitor_speed=115200,
        description="Arduino Nano (ATmega328P) + ESP8266 + esp-link (Wi-Fi↔UART bridge)",
        hardware_components=[
            "Arduino Nano (ATmega328P)",
            "ESP8266 모듈",
            "esp-link 펌웨어",
        ],
        connection_guide="""
하드웨어 연결:
1. ESP8266에 esp-link 펌웨어 플래시
2. Arduino Nano와 ESP8266 연결:
   - Arduino Nano TX → ESP8266 RX
   - Arduino Nano RX → ESP8266 TX
   - 공통 GND 연결
   - ESP8266 VCC → 3.3V (주의: 5V 연결 금지!)

esp-link 설정:
1. ESP8266의 AP 모드로 접속 (기본 SSID: "ESP_xxxxxx")
2. 웹 브라우저에서 192.168.4.1 접속
3. Wi-Fi 설정 및 UART 설정 (Baud rate: 115200)
        """,
    ),
    ArduinoTargetType.NANO_STANDALONE: ArduinoTargetConfig(
        target_type=ArduinoTargetType.NANO_STANDALONE,
        board_name="nanoatmega328",
        platform="atmelavr",
        framework="arduino",
        monitor_speed=115200,
        description="Arduino Nano (ATmega328P) 단독 - USB 케이블 직접 연결 (wired)",
        hardware_components=["Arduino Nano (ATmega328P)", "USB 케이블"],
        connection_guide="""
하드웨어 연결:
1. Arduino Nano를 USB 케이블로 Xavier의 USB 포트에 연결
2. Arduino Nano의 전원 LED 확인
3. USB 케이블이 데이터 전송을 지원하는지 확인 (충전 전용 케이블 제외)

시리얼 포트 확인:
- /dev/ttyUSB0 (CH340, CP2102 등 USB-to-Serial 칩)
- /dev/ttyACM0 (Arduino Uno/Nano의 ATmega16U2)

권한 확인:
- dialout 그룹에 사용자 추가됨 (재로그인 필요)
- udev 규칙 설정됨
        """,
    ),
    ArduinoTargetType.UNO: ArduinoTargetConfig(
        target_type=ArduinoTargetType.UNO,
        board_name="uno",
        platform="atmelavr",
        framework="arduino",
        monitor_speed=115200,
        description="Arduino Uno",
        hardware_components=["Arduino Uno"],
    ),
    ArduinoTargetType.ESP32_DEV: ArduinoTargetConfig(
        target_type=ArduinoTargetType.ESP32_DEV,
        board_name="esp32dev",
        platform="espressif32",
        framework="arduino",
        monitor_speed=115200,
        description="ESP32 Dev Board",
        hardware_components=["ESP32 Dev Board"],
    ),
    ArduinoTargetType.NANO_ESP32: ArduinoTargetConfig(
        target_type=ArduinoTargetType.NANO_ESP32,
        board_name="nano_esp32",
        platform="espressif32",
        framework="arduino",
        monitor_speed=115200,
        description="Arduino Nano ESP32",
        hardware_components=["Arduino Nano ESP32"],
    ),
}


def get_arduino_target_config(target_type: ArduinoTargetType) -> Optional[ArduinoTargetConfig]:
    """타겟 타입에 해당하는 구성 정보 반환"""
    return ARDUINO_TARGET_CONFIGS.get(target_type)


def get_all_target_types() -> List[ArduinoTargetType]:
    """모든 지원되는 타겟 타입 목록 반환"""
    return list(ARDUINO_TARGET_CONFIGS.keys())


def get_platformio_ini_for_target(target_type: ArduinoTargetType) -> str:
    """타겟 타입에 맞는 platformio.ini 환경 설정 반환"""
    config = get_arduino_target_config(target_type)
    if not config:
        return ""
    
    return f"""[env:{config.platformio_env}]
platform = {config.platform}
board = {config.board_name}
framework = {config.framework}
monitor_speed = {config.monitor_speed}
"""


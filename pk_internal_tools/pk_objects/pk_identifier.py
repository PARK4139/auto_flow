import logging
from enum import Enum

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name


class PkDevice(Enum):
    asus_desktop = "asus_desktop"
    jetson_agx_xavier = "jetson_agx_xavier"
    esp32_dev = "esp32_dev"
    arduino_nano = "arduino_nano(Atmege328P)"
    arduino_nano_esp32 = "arduino_nano_esp32"
    jetson_nano = "jetson_nano"
    ras_berry_pi_4_b_plus = "ras_berry_pi_4_b_plus"
    undefined = "undefined"


class PkIdentifier:
    """
    디바이스 기본 식별 정보만 제공하는 단순한 클래스
    - identifier: 디바이스의 고유 식별자 (PkDevice enum)
    - nick_name: 디바이스의 별명
    """
    
    def __init__(self, identifier: "PkDevice", nick_name: str = None):
        """
        공통 속성 초기화
        
        Args:
            identifier: 디바이스의 고유 식별자 (PkDevice enum)
            nick_name: 디바이스의 별명 (없으면 기본값 생성)
        """
        self._identifier = identifier
        self._nick_name = nick_name or f"device_{identifier.value}"
        caller_n = get_caller_name()
        logging.debug(f'{caller_n} initialized: identifier={identifier.value}, nick_name={self._nick_name}')

    @property
    def identifier(self) -> "PkDevice":
        """디바이스의 고유 식별자를 가져옵니다."""
        return self._identifier

    @property
    def nick_name(self) -> str:
        """디바이스의 별명을 가져옵니다."""
        return self._nick_name

    @nick_name.setter
    def nick_name(self, value: str):
        """디바이스의 별명을 설정합니다."""
        self._nick_name = value
    
    def __str__(self):
        return f"{self.nick_name} (ID: {self.identifier.value})"

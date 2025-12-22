"""
pk_device 레지스트리 시스템
- 디바이스 중복 등록 방지
- identifier를 고유 ID로 사용
"""

import logging
from typing import Dict, Optional
from pk_internal_tools.pk_objects.pk_identifier import PkDevice


class PkDeviceRegistry:
    """
    pk_device 전역 레지스트리
    identifier를 고유 ID로 사용하여 디바이스 정보를 저장하고 가져옵니다.
    identifier가 동일하면 저장된 디바이스 정보를 가져옵니다.
    """
    
    _instance: Optional['PkDeviceRegistry'] = None
    _devices: Dict[PkDevice, object] = {}  # identifier -> controller 객체
    _targets: Dict[PkDevice, dict] = {}  # identifier -> target config dict
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._devices = {}
            cls._instance._targets = {}
        return cls._instance
    
    def register(self, identifier: PkDevice, device: object, target_config: dict = None) -> None:
        """
        디바이스를 레지스트리에 등록 (또는 업데이트)
        
        Args:
            identifier: 디바이스의 고유 식별자 (PkDevice enum)
            device: 등록할 디바이스 객체
            target_config: target 설정 dict (선택적)
        """
        self._devices[identifier] = device
        if target_config:
            self._targets[identifier] = target_config.copy()
        logging.debug(f"디바이스 등록/업데이트 성공: identifier='{identifier.value}', device={device}")
    
    def get_or_register(self, identifier: PkDevice, device_factory=None) -> tuple[Optional[object], Optional[dict]]:
        """
        identifier로 저장된 디바이스 정보를 가져오거나, 없으면 새로 등록
        
        Args:
            identifier: 디바이스의 고유 식별자
            device_factory: 디바이스를 생성하는 함수 (선택적)
            
        Returns:
            tuple: (controller 객체, target_config dict)
        """
        if identifier in self._targets:
            # 저장된 target 정보가 있으면 반환
            stored_controller = self._devices.get(identifier)
            stored_target = self._targets[identifier]
            logging.debug(f"저장된 디바이스 정보 반환: identifier='{identifier.value}'")
            return stored_controller, stored_target
        else:
            # 없으면 None 반환 (새로 생성해야 함)
            return None, None
    
    def unregister(self, identifier: PkDevice) -> bool:
        """
        디바이스를 레지스트리에서 제거
        
        Args:
            identifier: 제거할 디바이스의 identifier
            
        Returns:
            bool: 제거 성공 여부
        """
        if identifier in self._devices:
            device = self._devices.pop(identifier)
            logging.debug(f"디바이스 제거 성공: identifier='{identifier.value}', device={device}")
            return True
        else:
            logging.warning(f"디바이스 제거 실패: identifier '{identifier.value}'가 레지스트리에 없습니다.")
            return False
    
    def is_registered(self, identifier: PkDevice) -> bool:
        """
        identifier가 이미 등록되어 있는지 확인
        
        Args:
            identifier: 확인할 identifier
            
        Returns:
            bool: 등록 여부
        """
        return identifier in self._devices
    
    def get_device(self, identifier: PkDevice) -> Optional[object]:
        """
        identifier로 디바이스 객체 가져오기
        
        Args:
            identifier: 찾을 디바이스의 identifier
            
        Returns:
            디바이스 객체 또는 None
        """
        return self._devices.get(identifier)
    
    def get_target_config(self, identifier: PkDevice) -> Optional[dict]:
        """
        identifier로 저장된 target 설정 dict 가져오기
        
        Args:
            identifier: 찾을 디바이스의 identifier
            
        Returns:
            target 설정 dict 또는 None
        """
        return self._targets.get(identifier)
    
    def get_all_devices(self) -> Dict[PkDevice, object]:
        """
        등록된 모든 디바이스 반환
        
        Returns:
            Dict[PkDevice, object]: identifier -> device 객체 매핑
        """
        return self._devices.copy()
    
    def clear(self) -> None:
        """모든 디바이스 제거 (테스트용)"""
        self._devices.clear()
        logging.debug("레지스트리 초기화 완료")


# 전역 레지스트리 인스턴스
device_registry = PkDeviceRegistry()


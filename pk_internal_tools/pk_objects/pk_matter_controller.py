#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PK Matter Controller - python-matter-server 기능을 효율적으로 활용하는 클래스

python-matter-server의 WebSocket API를 래핑하여 더 쉽고 직관적으로 Matter 장치를 제어할 수 있도록 합니다.
"""

import asyncio
import json
import uuid
import logging
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked

# Lazy imports
try:
    import websockets
except ImportError:
    websockets = None


class MatterDeviceType(Enum):
    """Matter 장치 타입 열거형"""
    SMART_PLUG = "smart_plug"
    LIGHT_BULB = "light_bulb"
    SWITCH = "switch"
    SENSOR = "sensor"
    UNKNOWN = "unknown"


@dataclass
class MatterDevice:
    """Matter 장치 정보를 담는 데이터 클래스"""
    node_id: int
    vendor_name: str = ""
    product_name: str = ""
    device_type: MatterDeviceType = MatterDeviceType.UNKNOWN
    is_online: bool = False
    
    @property
    def display_name(self) -> str:
        """장치 표시명"""
        if self.product_name:
            return f"{self.vendor_name} {self.product_name}".strip()
        return f"Matter Device {self.node_id}"
    
    def __str__(self) -> str:
        return f"MatterDevice(id={self.node_id}, name='{self.display_name}', type={self.device_type.value})"


@dataclass
class MatterCommissionConfig:
    """Matter 장치 커미션 설정"""
    commission_code: str
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    use_ble: bool = True
    timeout_seconds: int = 120


class PkMatterController:
    """
    PK Matter Controller - python-matter-server를 효율적으로 활용하는 컨트롤러 클래스
    
    주요 기능:
    - Matter 서버 자동 시작/중지
    - 장치 자동 발견 및 관리
    - 직관적인 장치 제어 API
    - 비동기 작업 지원
    - 자동 재연결 및 오류 복구
    """
    
    def __init__(self, server_url: str = "ws://localhost:5580/ws", auto_start_server: bool = True):
        """
        PK Matter Controller 초기화
        
        Args:
            server_url: Matter 서버 WebSocket URL
            auto_start_server: 서버가 실행되지 않은 경우 자동으로 시작할지 여부
        """
        self.server_url = server_url
        self.auto_start_server = auto_start_server
        self.ws = None
        self.devices: Dict[int, MatterDevice] = {}
        self.is_connected = False
        self._server_process = None
        
        # 로깅 설정
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.disconnect()
    
    async def connect(self) -> bool:
        """Matter 서버에 연결"""
        try:
            # websockets 모듈 확인 및 설치
            websockets_module = await self._ensure_websockets_module()
            if not websockets_module:
                return False
            
            # 서버 실행 상태 확인
            if not await self._is_server_running():
                if self.auto_start_server:
                    self.logger.info("Matter 서버를 시작합니다...")
                    if not await self._start_server():
                        return False
                else:
                    self.logger.error("Matter 서버가 실행되지 않았습니다.")
                    return False
            
            # WebSocket 연결
            self.logger.info(f"Matter 서버에 연결 중: {self.server_url}")
            self.ws = await websockets_module.connect(
                self.server_url,
                max_size=2**22,
                ping_interval=30,
                ping_timeout=30
            )
            
            # 연결 확인 및 초기화
            await self._send_command("start_listening")
            await self.discover_devices()
            
            self.is_connected = True
            self.logger.info("Matter 서버 연결 완료")
            return True
            
        except Exception as e:
            self.logger.error(f"Matter 서버 연결 실패: {e}")
            return False
    
    async def disconnect(self):
        """Matter 서버 연결 해제"""
        if self.ws:
            try:
                await self.ws.close()
            except Exception as e:
                self.logger.warning(f"WebSocket 연결 해제 중 오류: {e}")
            self.ws = None
        
        self.is_connected = False
        self.logger.info("Matter 서버 연결 해제 완료")
    
    async def discover_devices(self) -> List[MatterDevice]:
        """연결된 Matter 장치들을 발견하고 목록을 업데이트"""
        try:
            response = await self._send_command("get_nodes")
            nodes = response.get("result", [])
            
            self.devices.clear()
            for node_data in nodes:
                device = self._parse_device_data(node_data)
                self.devices[device.node_id] = device
                self.logger.info(f"발견된 장치: {device}")
            
            self.logger.info(f"총 {len(self.devices)}개의 Matter 장치를 발견했습니다.")
            return list(self.devices.values())
            
        except Exception as e:
            self.logger.error(f"장치 발견 실패: {e}")
            return []
    
    def get_devices(self) -> List[MatterDevice]:
        """현재 발견된 장치 목록 반환"""
        return list(self.devices.values())
    
    def get_device(self, node_id: int) -> Optional[MatterDevice]:
        """특정 node_id의 장치 정보 반환"""
        return self.devices.get(node_id)
    
    def find_devices_by_type(self, device_type: MatterDeviceType) -> List[MatterDevice]:
        """특정 타입의 장치들을 찾아서 반환"""
        return [device for device in self.devices.values() if device.device_type == device_type]
    
    def find_device_by_name(self, name: str, partial_match: bool = True) -> Optional[MatterDevice]:
        """이름으로 장치 찾기"""
        for device in self.devices.values():
            if partial_match:
                if name.lower() in device.display_name.lower():
                    return device
            else:
                if name.lower() == device.display_name.lower():
                    return device
        return None
    
    async def commission_device(self, config: MatterCommissionConfig) -> bool:
        """새로운 Matter 장치를 커미션"""
        try:
            self.logger.info(f"장치 커미션 시작: {ensure_sensitive_info_masked(config.commission_code)}")
            
            # Wi-Fi 자격 증명 설정 (필요한 경우)
            if config.wifi_ssid and config.wifi_password:
                self.logger.info(f"Wi-Fi 자격 증명 설정: {ensure_sensitive_info_masked(config.wifi_ssid)}")
                await self._send_command("set_wifi_credentials", {
                    "ssid": config.wifi_ssid,
                    "credentials": config.wifi_password
                })
                await asyncio.sleep(1.0)  # 설정 적용 대기
            
            # 커미션 실행
            response = await self._send_command("commission_with_code", {
                "code": config.commission_code
            })
            
            if response.get("result"):
                self.logger.info("장치 커미션 성공")
                await self.discover_devices()  # 장치 목록 업데이트
                return True
            else:
                self.logger.error(f"장치 커미션 실패: {response}")
                return False
                
        except Exception as e:
            self.logger.error(f"장치 커미션 중 오류: {e}")
            return False
    
    async def turn_on(self, node_id: int) -> bool:
        """장치 켜기"""
        return await self._set_onoff(node_id, True)
    
    async def turn_off(self, node_id: int) -> bool:
        """장치 끄기"""
        return await self._set_onoff(node_id, False)
    
    async def toggle(self, node_id: int) -> bool:
        """장치 상태 토글"""
        current_state = await self.get_onoff_state(node_id)
        if current_state is None:
            return False
        return await self._set_onoff(node_id, not current_state)
    
    async def get_onoff_state(self, node_id: int) -> Optional[bool]:
        """장치의 on/off 상태 확인"""
        try:
            response = await self._send_command("read_attribute", {
                "node_id": node_id,
                "attribute_path": "1/6/0"  # endpoint/cluster/attribute
            })
            
            result = response.get("result")
            if result is not None:
                return bool(result.get("value"))
            return None
            
        except Exception as e:
            self.logger.error(f"상태 읽기 실패 (node_id={node_id}): {e}")
            return None
    
    async def _set_onoff(self, node_id: int, state: bool) -> bool:
        """장치의 on/off 상태 설정"""
        try:
            device = self.get_device(node_id)
            action = "켜기" if state else "끄기"
            device_name = device.display_name if device else f"장치 {node_id}"
            
            self.logger.info(f"{device_name} {action} 시도")
            
            response = await self._send_command("write_attribute", {
                "node_id": node_id,
                "attribute_path": "1/6/0",  # endpoint/cluster/attribute
                "value": state
            })
            
            if response.get("result") is not None:
                self.logger.info(f"{device_name} {action} 성공")
                return True
            else:
                self.logger.error(f"{device_name} {action} 실패: {response}")
                return False
                
        except Exception as e:
            self.logger.error(f"장치 제어 실패 (node_id={node_id}, state={state}): {e}")
            return False
    
    async def _send_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """WebSocket을 통해 명령어 전송"""
        if not self.ws:
            raise Exception("WebSocket 연결이 없습니다.")
        
        message = {
            "message_id": str(uuid.uuid4()),
            "command": command
        }
        if args:
            message["args"] = args
        
        payload = json.dumps(message)
        await self.ws.send(payload)
        self.logger.debug(f"→ {payload}")
        
        response = await self.ws.recv()
        self.logger.debug(f"← {response}")
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "invalid_json_response", "raw": response}
    
    def _parse_device_data(self, node_data: Dict[str, Any]) -> MatterDevice:
        """서버에서 받은 노드 데이터를 MatterDevice 객체로 변환"""
        node_id = int(node_data.get("node_id", 0))
        vendor_name = node_data.get("vendor_name", "")
        product_name = node_data.get("product_name", "")
        
        # 장치 타입 추론
        device_type = MatterDeviceType.UNKNOWN
        product_lower = product_name.lower()
        vendor_lower = vendor_name.lower()
        
        if "plug" in product_lower or "outlet" in product_lower:
            device_type = MatterDeviceType.SMART_PLUG
        elif "light" in product_lower or "bulb" in product_lower or "lamp" in product_lower:
            device_type = MatterDeviceType.LIGHT_BULB
        elif "switch" in product_lower:
            device_type = MatterDeviceType.SWITCH
        elif "sensor" in product_lower:
            device_type = MatterDeviceType.SENSOR
        
        return MatterDevice(
            node_id=node_id,
            vendor_name=vendor_name,
            product_name=product_name,
            device_type=device_type,
            is_online=True  # 발견된 장치는 온라인으로 가정
        )
    
    async def _is_server_running(self) -> bool:
        """Matter 서버 실행 상태 확인"""
        try:
            # aiohttp 사용 시도
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://localhost:5580", timeout=aiohttp.ClientTimeout(total=5)) as response:
                        return response.status == 200
            except ImportError:
                # aiohttp가 없으면 기존 방식 사용
                from pk_internal_tools.pk_functions.ensure_matter_server_managed import is_matter_server_running
                return await is_matter_server_running()
        except Exception as e:
            self.logger.debug(f"서버 상태 확인 실패: {e}")
            return False
    
    async def _start_server(self) -> bool:
        """Matter 서버 시작"""
        try:
            # 서버 시작 로직은 기존 ensure_matter_smart_plug_on.py의 로직을 활용
            from pk_internal_tools.pk_functions.ensure_matter_server_managed import ensure_matter_server_running
            
            success, process = await ensure_matter_server_running()
            if success:
                self._server_process = process
                # 서버 준비 대기
                await asyncio.sleep(5)
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Matter 서버 시작 실패: {e}")
            return False
    
    async def _ensure_websockets_module(self):
        """websockets 모듈 확인 및 설치"""
        try:
            # 먼저 import 시도
            import websockets
            return websockets
        except ImportError:
            self.logger.info("websockets 모듈을 설치합니다...")
            
            # 설치 시도
            await self._install_package("websockets")
            
            # 재import 시도
            try:
                import websockets
                return websockets
            except ImportError as e:
                self.logger.error(f"websockets 모듈 설치 후에도 import 실패: {e}")
                return None

    async def _install_package(self, package_name: str):
        """필요한 패키지 설치"""
        import subprocess
        import sys
        
        try:
            # 비동기적으로 subprocess 실행
            process = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "pip", "install", package_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise subprocess.CalledProcessError(process.returncode, [sys.executable, "-m", "pip", "install", package_name], error_msg)
                
            self.logger.info(f"패키지 설치 성공: {package_name}")
            
        except Exception as e:
            self.logger.error(f"패키지 설치 실패 ({package_name}): {e}")
            raise


# 편의 함수들
async def create_matter_controller(server_url: str = "ws://localhost:5580/ws") -> PkMatterController:
    """Matter 컨트롤러 생성 및 연결"""
    controller = PkMatterController(server_url)
    await controller.connect()
    return controller


async def quick_device_control(node_id: int, action: str) -> bool:
    """빠른 장치 제어 (일회성 작업용)"""
    async with PkMatterController() as controller:
        if action.lower() == "on":
            return await controller.turn_on(node_id)
        elif action.lower() == "off":
            return await controller.turn_off(node_id)
        elif action.lower() == "toggle":
            return await controller.toggle(node_id)
        else:
            raise ValueError(f"지원하지 않는 액션: {action}")


# 사용 예시
if __name__ == "__main__":
    async def main():
        """사용 예시"""
        # n. 컨텍스트 매니저 사용
        async with PkMatterController() as controller:
            # 장치 발견
            devices = await controller.discover_devices()
            logging.debug(f"발견된 장치: {len(devices)}개")
            
            for device in devices:
                logging.debug(f"{device}")
                
                # 상태 확인
                state = await controller.get_onoff_state(device.node_id)
                logging.debug(f"현재 상태: {'ON' if state else 'OFF' if state is not None else 'UNKNOWN'}")
                
                # 장치 제어 (예: 켜기)
                if await controller.turn_on(device.node_id):
                    logging.debug(f"{device.display_name} 켜기 성공")
        
        # n. 빠른 제어
        success = await quick_device_control(1, "toggle")
        logging.debug(f"빠른 제어 결과: {success}")
    
    # 실행
    asyncio.run(main())

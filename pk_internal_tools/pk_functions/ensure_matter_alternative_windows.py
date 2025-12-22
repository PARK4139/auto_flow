#!/usr/bin/env python3

"""
Windows용 Matter 제어 대안 솔루션

Windows에서 home-assistant-chip-core가 지원되지 않으므로 대안적인 방법들을 제공합니다.
"""

import asyncio
import logging
import subprocess
import json
import time
from typing import Optional, Dict, Any, List
from pathlib import Path


class WindowsMatterAlternative:
    """Windows용 Matter 제어 대안 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def control_via_chip_tool(self, node_id: int, action: str) -> bool:
        """
        chip-tool을 사용한 Matter 장치 제어
        
        Args:
            node_id: 장치 노드 ID
            action: 수행할 액션 ("on", "off", "toggle", "status")
            
        Returns:
            bool: 성공 여부
        """
        
        try:
            # chip-tool 경로 확인
            chip_tool_path = await self._find_chip_tool()
            if not chip_tool_path:
                self.logger.error("chip-tool을 찾을 수 없습니다.")
                return False
            
            # 명령어 구성
            if action == "on":
                cmd = [str(chip_tool_path), "onoff", "on", str(node_id), "1"]
            elif action == "off":
                cmd = [str(chip_tool_path), "onoff", "off", str(node_id), "1"]
            elif action == "toggle":
                cmd = [str(chip_tool_path), "onoff", "toggle", str(node_id), "1"]
            elif action == "status":
                cmd = [str(chip_tool_path), "onoff", "read", "on-off", str(node_id), "1"]
            else:
                self.logger.error(f"지원하지 않는 액션: {action}")
                return False
            
            # 명령어 실행
            self.logger.info(f"chip-tool 명령어 실행: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.logger.info(f"chip-tool 명령어 성공: {action}")
                if stdout:
                    self.logger.debug(f"출력: {stdout.decode()}")
                return True
            else:
                self.logger.error(f"chip-tool 명령어 실패: {stderr.decode()}")
                return False
                
        except Exception as e:
            self.logger.error(f"chip-tool 실행 중 오류: {e}")
            return False
    
    async def control_via_rest_api(self, device_ip: str, action: str) -> bool:
        """
        REST API를 사용한 직접 장치 제어 (TP-Link Tapo 등)
        
        Args:
            device_ip: 장치 IP 주소
            action: 수행할 액션
            
        Returns:
            bool: 성공 여부
        """
        
        try:
            # aiohttp 사용 (설치되어 있는 경우)
            try:
                import aiohttp
                
                async with aiohttp.ClientSession() as session:
                    # TP-Link Tapo P110M의 경우 예시
                    url = f"http://{device_ip}/api/v1/device"
                    
                    if action == "on":
                        payload = {"device_on": True}
                    elif action == "off":
                        payload = {"device_on": False}
                    elif action == "status":
                        # 상태 조회
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                state = data.get("device_on", False)
                                self.logger.info(f"장치 상태: {'ON' if state else 'OFF'}")
                                return True
                            return False
                    else:
                        self.logger.error(f"지원하지 않는 액션: {action}")
                        return False
                    
                    # 제어 명령 전송
                    async with session.post(url, json=payload) as response:
                        success = response.status == 200
                        if success:
                            self.logger.info(f"REST API 제어 성공: {action}")
                        else:
                            self.logger.error(f"REST API 제어 실패: {response.status}")
                        return success
                        
            except ImportError:
                self.logger.warning("aiohttp가 설치되지 않아 REST API를 사용할 수 없습니다.")
                return False
                
        except Exception as e:
            self.logger.error(f"REST API 제어 중 오류: {e}")
            return False
    
    async def control_via_mqtt(self, topic: str, action: str) -> bool:
        """
        MQTT를 사용한 Matter 장치 제어
        
        Args:
            topic: MQTT 토픽
            action: 수행할 액션
            
        Returns:
            bool: 성공 여부
        """
        
        try:
            # paho-mqtt 사용 (설치되어 있는 경우)
            try:
                import paho.mqtt.client as mqtt
                
                # MQTT 클라이언트 설정
                client = mqtt.Client()
                
                # 메시지 발행
                if action == "on":
                    message = "ON"
                elif action == "off":
                    message = "OFF"
                elif action == "toggle":
                    message = "TOGGLE"
                else:
                    self.logger.error(f"지원하지 않는 액션: {action}")
                    return False
                
                # MQTT 브로커에 연결 (로컬 브로커 가정)
                client.connect("localhost", 1883, 60)
                
                # 메시지 발행
                result = client.publish(topic, message)
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    self.logger.info(f"MQTT 메시지 발행 성공: {topic} -> {message}")
                    return True
                else:
                    self.logger.error(f"MQTT 메시지 발행 실패: {result.rc}")
                    return False
                    
            except ImportError:
                self.logger.warning("paho-mqtt가 설치되지 않아 MQTT를 사용할 수 없습니다.")
                return False
                
        except Exception as e:
            self.logger.error(f"MQTT 제어 중 오류: {e}")
            return False
    
    async def control_via_http_bridge(self, bridge_url: str, node_id: int, action: str) -> bool:
        """
        HTTP 브리지를 통한 Matter 제어 (다른 시스템에서 실행 중인 Matter 서버)
        
        Args:
            bridge_url: Matter 브리지 서버 URL
            node_id: 장치 노드 ID
            action: 수행할 액션
            
        Returns:
            bool: 성공 여부
        """
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                url = f"{bridge_url}/api/matter/device/{node_id}/{action}"
                
                async with session.post(url) as response:
                    success = response.status == 200
                    
                    if success:
                        self.logger.info(f"HTTP 브리지 제어 성공: {action}")
                        data = await response.json()
                        self.logger.debug(f"응답: {data}")
                    else:
                        self.logger.error(f"HTTP 브리지 제어 실패: {response.status}")
                        error_text = await response.text()
                        self.logger.debug(f"오류 응답: {error_text}")
                    
                    return success
                    
        except Exception as e:
            self.logger.error(f"HTTP 브리지 제어 중 오류: {e}")
            return False
    
    async def _find_chip_tool(self) -> Optional[Path]:
        """chip-tool 실행파일 찾기"""
        
        # 일반적인 chip-tool 위치들
        possible_paths = [
            Path("chip-tool.exe"),
            Path("chip-tool"),
            Path.home() / "matter" / "chip-tool.exe",
            Path.home() / "matter" / "chip-tool",
            Path("C:/matter/chip-tool.exe"),
            Path("C:/Program Files/matter/chip-tool.exe"),
        ]
        
        # PATH에서 찾기
        try:
            result = subprocess.run(["where", "chip-tool"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return Path(result.stdout.strip().split('\n')[0])
        except Exception as e:
            pass
        
        # 가능한 경로들 확인
        for path in possible_paths:
            if path.exists():
                return path
        
        return None


# 편의 함수들
async def control_matter_device_windows(
    node_id: int = 1,
    action: str = "toggle",
    method: str = "auto",
    **kwargs
) -> bool:
    """
    Windows에서 Matter 장치 제어
    
    Args:
        node_id: 장치 노드 ID
        action: 수행할 액션 ("on", "off", "toggle", "status")
        method: 제어 방법 ("auto", "chip-tool", "rest", "mqtt", "bridge")
        **kwargs: 각 방법별 추가 파라미터
        
    Returns:
        bool: 성공 여부
    """
    
    controller = WindowsMatterAlternative()
    
    if method == "auto":
        # 자동으로 사용 가능한 방법 시도
        methods_to_try = ["chip-tool", "rest", "mqtt", "bridge"]
    else:
        methods_to_try = [method]
    
    for method_name in methods_to_try:
        try:
            if method_name == "chip-tool":
                success = await controller.control_via_chip_tool(node_id, action)
            elif method_name == "rest":
                device_ip = kwargs.get("device_ip", "192.168.1.100")
                success = await controller.control_via_rest_api(device_ip, action)
            elif method_name == "mqtt":
                topic = kwargs.get("topic", f"matter/device/{node_id}")
                success = await controller.control_via_mqtt(topic, action)
            elif method_name == "bridge":
                bridge_url = kwargs.get("bridge_url", "http://localhost:8080")
                success = await controller.control_via_http_bridge(bridge_url, node_id, action)
            else:
                continue
            
            if success:
                logging.info(f"Matter 장치 제어 성공 (방법: {method_name})")
                return True
                
        except Exception as e:
            logging.warning(f"{method_name} 방법 실패: {e}")
            continue
    
    logging.error("모든 제어 방법이 실패했습니다.")
    return False


def control_matter_device_windows_sync(
    node_id: int = 1,
    action: str = "toggle",
    method: str = "auto",
    **kwargs
) -> bool:
    """동기 버전의 Windows Matter 장치 제어"""
    return asyncio.run(control_matter_device_windows(node_id, action, method, **kwargs))


# P110M 전용 편의 함수들
async def control_p110m_windows(action: str = "toggle", **kwargs) -> bool:
    """P110M 전용 Windows 제어 함수"""
    return await control_matter_device_windows(node_id=1, action=action, **kwargs)


def control_p110m_windows_sync(action: str = "toggle", **kwargs) -> bool:
    """P110M 전용 Windows 제어 함수 (동기 버전)"""
    return asyncio.run(control_p110m_windows(action, **kwargs))


if __name__ == "__main__":
    async def test_windows_alternatives():
        """Windows 대안 방법들 테스트"""
        
        logging.basicConfig(level=logging.INFO)
        
        print("=== Windows Matter 제어 대안 테스트")
        
        # n. chip-tool 테스트
        print("1. chip-tool 방법 테스트:")
        success = await control_matter_device_windows(1, "status", "chip-tool")
        print(f"   결과: {'성공' if success else '실패'}")
        
        # n. REST API 테스트 (예시 IP)
        print("2. REST API 방법 테스트:")
        success = await control_matter_device_windows(
            1, "status", "rest", device_ip="192.168.1.100"
        )
        print(f"   결과: {'성공' if success else '실패'}")
        
        # n. 자동 방법 테스트
        print("3. 자동 방법 테스트:")
        success = await control_matter_device_windows(1, "status", "auto")
        print(f"   결과: {'성공' if success else '실패'}")
        
        print("=== 테스트 완료")
    
    # 테스트 실행
    asyncio.run(test_windows_alternatives())

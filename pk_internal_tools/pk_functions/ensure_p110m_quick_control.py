#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P110M 빠른 제어 - 네트워크 스캔 없이 빠르게 제어하는 방법들

네트워크 스캔으로 인한 지연을 피하고, 더 빠르고 안정적인 P110M 제어 방법을 제공합니다.
"""

import asyncio
import logging
import subprocess
import json
import socket
import struct
import time
from typing import Optional, Dict, Any, List
from pathlib import Path


class P110MQuickController:
    """P110M 빠른 제어 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_common_router_ips(self) -> List[str]:
        """일반적인 라우터 IP 대역들을 반환"""
        common_networks = [
            "192.168.1.",
            "192.168.0.", 
            "192.168.2.",
            "10.0.0.",
            "10.0.1.",
            "172.16.0.",
        ]
        
        ips = []
        for network in common_networks:
            # 일반적인 IoT 장치 IP 범위
            for i in [100, 101, 102, 103, 104, 105, 110, 111, 112, 113, 114, 115, 120, 150, 200]:
                ips.append(f"{network}{i}")
        
        return ips
    
    async def find_p110m_by_arp(self) -> List[str]:
        """ARP 테이블에서 TP-Link 장치 IP만 빠르게 찾기"""
        devices = []
        
        try:
            # Windows ARP 테이블 조회
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'dynamic' in line.lower():
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            ip = parts[0]
                            mac = parts[1].replace('-', ':').upper()
                            
                            # TP-Link MAC 주소 OUI 확인 (P110M의 실제 MAC 포함)
                            if mac.startswith(('BC:07:1D', '50:C7:BF', '98:DA:C4', 'AC:84:C6', 'BC-07-1D')):
                                devices.append(ip)
                                self.logger.info(f"ARP에서 TP-Link 장치 발견: {ip} ({mac})")
        
        except Exception as e:
            self.logger.debug(f"ARP 검색 오류: {e}")
        
        return devices
    
    async def test_kasa_connection(self, ip: str, timeout: float = 3.0) -> bool:
        """특정 IP에서 Kasa 프로토콜 연결 테스트"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((ip, 9999))  # Kasa 포트
            sock.close()
            
            if result == 0:
                self.logger.info(f"Kasa 프로토콜 연결 가능: {ip}")
                return True
        except Exception as e:
            self.logger.debug(f"Kasa 연결 테스트 실패 ({ip}): {e}")
        
        return False
    
    async def control_via_kasa_protocol(self, ip: str, action: str) -> bool:
        """Kasa 프로토콜을 사용한 직접 제어"""
        
        try:
            # TP-Link Kasa 프로토콜 명령어
            commands = {
                'info': '{"system":{"get_sysinfo":{}}}',
                'on': '{"system":{"set_relay_state":{"state":1}}}',
                'off': '{"system":{"set_relay_state":{"state":0}}}',
                'status': '{"system":{"get_sysinfo":{}}}'
            }
            
            if action not in commands:
                self.logger.error(f"지원하지 않는 액션: {action}")
                return False
            
            command = commands[action]
            
            # Kasa 프로토콜 암호화
            encrypted = self._encrypt_kasa_command(command)
            
            # TCP 소켓으로 명령 전송
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            try:
                self.logger.info(f"Kasa 프로토콜로 {ip}에 {action} 명령 전송...")
                sock.connect((ip, 9999))  # Kasa 기본 포트
                sock.send(encrypted)
                
                # 응답 수신
                data = sock.recv(2048)
                response = self._decrypt_kasa_response(data)
                
                self.logger.debug(f"Kasa 프로토콜 응답: {response}")
                
                if action in ['on', 'off']:
                    # 제어 명령의 경우 성공 여부 확인
                    try:
                        result = json.loads(response)
                        error_code = result.get('system', {}).get('set_relay_state', {}).get('err_code', -1)
                        if error_code == 0:
                            self.logger.info(f"✅ P110M {action} 성공")
                            return True
                        else:
                            self.logger.error(f"❌ P110M {action} 실패: error_code={error_code}")
                            return False
                    except json.JSONDecodeError:
                        # JSON 파싱 실패해도 명령은 전송되었을 수 있음
                        self.logger.warning(f"응답 파싱 실패, 하지만 {action} 명령은 전송됨")
                        return True
                else:
                    # 상태 조회의 경우
                    try:
                        result = json.loads(response)
                        sysinfo = result.get('system', {}).get('get_sysinfo', {})
                        relay_state = sysinfo.get('relay_state', -1)
                        device_name = sysinfo.get('alias', 'P110M')
                        
                        if relay_state != -1:
                            state_text = "ON" if relay_state == 1 else "OFF"
                            self.logger.info(f"📊 {device_name} 현재 상태: {state_text}")
                            
                            # 추가 정보도 출력
                            if 'rssi' in sysinfo:
                                self.logger.info(f"📶 신호 강도: {sysinfo['rssi']} dBm")
                            
                            return True
                    except json.JSONDecodeError:
                        self.logger.warning("상태 응답 파싱 실패")
                    
                    return True
                
            finally:
                sock.close()
        
        except ConnectionRefusedError:
            self.logger.warning(f"❌ {ip}:9999에 연결할 수 없습니다 (장치가 없거나 Kasa 프로토콜 미지원)")
        except socket.timeout:
            self.logger.warning(f"❌ {ip} 연결 시간 초과")
        except Exception as e:
            self.logger.error(f"❌ Kasa 프로토콜 제어 오류 ({ip}): {e}")
        
        return False
    
    def _encrypt_kasa_command(self, command: str) -> bytes:
        """Kasa 프로토콜 명령어 암호화"""
        key = 171
        result = struct.pack('>I', len(command))
        
        for char in command:
            key ^= ord(char)
            result += bytes([key])
        
        return result
    
    def _decrypt_kasa_response(self, data: bytes) -> str:
        """Kasa 프로토콜 응답 복호화"""
        if len(data) < 4:
            return ""
        
        length = struct.unpack('>I', data[:4])[0]
        data = data[4:]
        
        key = 171
        result = ""
        
        for byte in data[:length]:
            key ^= byte
            result += chr(key)
        
        return result
    
    async def try_manual_ip_input(self) -> Optional[str]:
        """사용자에게 수동으로 IP 입력 받기"""
        
        print("🔧 P110M 장치를 자동으로 찾을 수 없습니다.")
        print("📱 다음 방법으로 P110M의 IP 주소를 확인할 수 있습니다:")
        print("   1. TP-Link Kasa 앱 → 장치 설정 → 장치 정보")
        print("   2. 라우터 관리 페이지에서 연결된 장치 목록 확인")
        print("   3. 스마트폰 Wi-Fi 설정에서 연결된 장치 확인")
        print()
        
        # 일반적인 IP들 제안
        common_ips = self.get_common_router_ips()[:10]  # 처음 10개만
        print("🎯 일반적인 P110M IP 주소들:")
        for i, ip in enumerate(common_ips, 1):
            print(f"   {i}. {ip}")
        print()
        
        try:
            user_input = input("P110M IP 주소를 입력하세요 (또는 Enter로 건너뛰기): ").strip()
            
            if user_input:
                # 간단한 IP 형식 검증
                parts = user_input.split('.')
                if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                    return user_input
                else:
                    print("❌ 올바른 IP 형식이 아닙니다.")
        except (KeyboardInterrupt, EOFError):
            print("⛔ 사용자 입력 취소")
        
        return None


# 메인 제어 함수들
async def control_p110m_quick(
    action: str = "toggle",
    target_ip: Optional[str] = None,
    try_common_ips: bool = True
) -> bool:
    """
    P110M 빠른 제어 함수
    
    Args:
        action: 수행할 액션 ("on", "off", "toggle", "status")
        target_ip: 특정 IP 지정 (None이면 자동 검색)
        try_common_ips: 일반적인 IP들도 시도할지 여부
        
    Returns:
        bool: 성공 여부
    """
    
    controller = P110MQuickController()
    
    # 시도할 IP 목록 구성
    ips_to_try = []
    
    # n. 지정된 IP가 있으면 최우선
    if target_ip:
        ips_to_try.append(target_ip)
        logging.info(f"지정된 IP 사용: {target_ip}")
    
    # n. ARP 테이블에서 TP-Link 장치 찾기
    arp_ips = await controller.find_p110m_by_arp()
    ips_to_try.extend(arp_ips)
    
    # n. 일반적인 IP들 추가 (옵션)
    if try_common_ips and not target_ip:
        common_ips = controller.get_common_router_ips()
        ips_to_try.extend(common_ips)
        logging.info(f"일반적인 IP {len(common_ips)}개 추가")
    
    # 중복 제거
    ips_to_try = list(dict.fromkeys(ips_to_try))  # 순서 유지하면서 중복 제거
    
    if not ips_to_try:
        logging.error("시도할 IP 주소가 없습니다.")
        return False
    
    logging.info(f"총 {len(ips_to_try)}개 IP 주소에서 P110M 검색 시작")
    
    # n. 각 IP에 대해 Kasa 프로토콜로 제어 시도
    for i, ip in enumerate(ips_to_try, 1):
        try:
            logging.info(f"[{i}/{len(ips_to_try)}] {ip} 시도 중...")
            
            # 빠른 연결 테스트 먼저
            if not await controller.test_kasa_connection(ip, timeout=2.0):
                continue
            
            # 실제 제어 시도
            success = await controller.control_via_kasa_protocol(ip, action)
            
            if success:
                logging.info(f"🎉 P110M 제어 성공! (IP: {ip}, 액션: {action})")
                return True
        
        except Exception as e:
            logging.debug(f"IP {ip} 시도 중 오류: {e}")
            continue
    
    # 모든 IP 실패 시
    logging.error("❌ 모든 IP 주소에서 P110M을 찾을 수 없습니다.")
    
    # 수동 입력 제안
    manual_ip = await controller.try_manual_ip_input()
    if manual_ip:
        logging.info(f"수동 입력된 IP로 재시도: {manual_ip}")
        success = await controller.control_via_kasa_protocol(manual_ip, action)
        if success:
            logging.info(f"🎉 수동 입력 IP로 P110M 제어 성공! (IP: {manual_ip})")
            return True
    
    # 최종 실패 안내
    logging.error("❌ P110M 제어에 실패했습니다.")
    logging.info("🔧 해결 방법:")
    logging.info("1. P110M이 같은 Wi-Fi 네트워크에 연결되어 있는지 확인")
    logging.info("2. TP-Link Kasa 앱에서 장치 상태 확인")
    logging.info("3. 라우터를 재시작하여 네트워크 문제 해결")
    logging.info("4. P110M 장치를 재시작 (전원 플러그 뽑았다 꽂기)")
    
    return False


def control_p110m_quick_sync(
    action: str = "toggle",
    target_ip: Optional[str] = None,
    try_common_ips: bool = True
) -> bool:
    """동기 버전의 P110M 빠른 제어"""
    return asyncio.run(control_p110m_quick(action, target_ip, try_common_ips))


# P110M 전용 편의 함수들
async def p110m_on(target_ip: Optional[str] = None) -> bool:
    """P110M 켜기"""
    return await control_p110m_quick("on", target_ip)


async def p110m_off(target_ip: Optional[str] = None) -> bool:
    """P110M 끄기"""
    return await control_p110m_quick("off", target_ip)


async def p110m_toggle(target_ip: Optional[str] = None) -> bool:
    """P110M 토글"""
    return await control_p110m_quick("toggle", target_ip)


async def p110m_status(target_ip: Optional[str] = None) -> bool:
    """P110M 상태 확인"""
    return await control_p110m_quick("status", target_ip)


def p110m_on_sync(target_ip: Optional[str] = None) -> bool:
    """P110M 켜기 (동기)"""
    return asyncio.run(p110m_on(target_ip))


def p110m_off_sync(target_ip: Optional[str] = None) -> bool:
    """P110M 끄기 (동기)"""
    return asyncio.run(p110m_off(target_ip))


def p110m_toggle_sync(target_ip: Optional[str] = None) -> bool:
    """P110M 토글 (동기)"""
    return asyncio.run(p110m_toggle(target_ip))


def p110m_status_sync(target_ip: Optional[str] = None) -> bool:
    """P110M 상태 확인 (동기)"""
    return asyncio.run(p110m_status(target_ip))


if __name__ == "__main__":
    async def test_quick_control():
        """빠른 제어 테스트"""
        
        logging.basicConfig(level=logging.INFO, 
                          format='[%(levelname)s] %(message)s')
        
        print("=== P110M 빠른 제어 테스트")
        
        # 상태 확인
        print("1. P110M 상태 확인:")
        await p110m_status()
        
        # 토글
        print("2. P110M 토글:")
        await p110m_toggle()
        
        print("=== 테스트 완료")
    
    # 테스트 실행
    asyncio.run(test_quick_control())

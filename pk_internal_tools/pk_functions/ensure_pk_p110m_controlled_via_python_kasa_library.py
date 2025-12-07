#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tapo 로컬 API를 통해 P110M을 직접 제어하는 함수.

Home Assistant 없이 로컬 네트워크에서 직접 P110M을 제어합니다.
python-kasa 또는 tapo 라이브러리를 사용합니다.

참고:
- python-kasa: https://python-kasa.readthedocs.io/
- tapo: https://pypi.org/project/tapo/
"""
import asyncio
import logging
import os
from typing import Optional, Dict, Any

from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
    ensure_env_var_completed_2025_11_24,
)
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)

# 모듈 레벨 변수: 같은 세션에서 controller와 연결 상태를 재사용
_cached_controller = None
_connection_verified = False
_cached_p110m_host = None


@ensure_seconds_measured
def ensure_python_kasa_installed() -> bool:
    """
    python-kasa 라이브러리가 설치되어 있는지 확인하고, 없으면 설치합니다.
    
    :return: 설치 성공 여부
    """
    try:
        import kasa
        logger.debug("python-kasa가 이미 설치되어 있습니다.")
        return True
    except ImportError:
        logger.info("python-kasa가 설치되어 있지 않습니다. 설치를 시작합니다...")
        
        try:
            import subprocess
            import sys
            
            # uv를 사용하는 경우
            if os.getenv("UV_VENV_PATH") or os.path.exists("pyproject.toml"):
                logger.info("uv를 사용하여 python-kasa 설치 중...")
                result = subprocess.run(
                    [sys.executable, "-m", "uv", "pip", "install", "python-kasa"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
            else:
                # 일반 pip 사용
                logger.info("pip를 사용하여 python-kasa 설치 중...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "python-kasa"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
            
            if result.returncode == 0:
                logger.info("python-kasa 설치 성공")
                return True
            else:
                logger.error("python-kasa 설치 실패: %s", result.stderr)
                return False
                
        except Exception as e:
            logger.error("python-kasa 설치 중 예외 발생: %s", e, exc_info=True)
            return False


@ensure_seconds_measured
async def _discover_p110m_devices() -> list[Dict[str, Any]]:
    """
    네트워크에서 P110M 장치를 발견합니다.
    
    python-kasa는 로컬 네트워크에서 자동으로 장치를 발견합니다.
    
    :return: 발견된 P110M 장치 목록
    """
    try:
        from kasa import Discover
        
        logger.info("네트워크에서 P110M 장치를 검색 중...")
        
        # python-kasa의 Discover 사용 (계정 정보 불필요)
        devices = await Discover.discover()
        
        p110m_devices = []
        for dev in devices.values():
            # P110M 또는 Tapo 플러그 필터링
            if "P110" in str(dev.model) or "Tapo" in str(dev.alias):
                p110m_devices.append({
                    "host": dev.host,
                    "alias": dev.alias,
                    "model": dev.model,
                    "device_type": type(dev).__name__,
                })
                logger.info("P110M 발견: %s (%s) - %s", dev.alias, dev.model, dev.host)
        
        return p110m_devices
        
    except Exception as e:
        logger.error("장치 발견 중 예외 발생: %s", e, exc_info=True)
        return []


@ensure_seconds_measured
async def _control_p110m_via_kasa(
    host: str,
    action: str,
) -> bool:
    """
    python-kasa를 사용하여 P110M을 제어합니다.
    
    python-kasa는 로컬 네트워크에서 직접 제어하므로 계정 정보가 필요 없습니다.
    
    :param host: P110M의 IP 주소
    :param action: 제어 액션 ("on", "off", "toggle", "status", "energy")
    :return: 성공 여부
    """
    try:
        from kasa import SmartPlug
        
        logger.info("P110M 연결 중: %s", host)
        plug = SmartPlug(host)
        
        # 현재 상태 업데이트
        await plug.update()
        
        current_state = plug.is_on
        logger.info("P110M 현재 상태: %s", "ON" if current_state else "OFF")
        
        if action == "status":
            logger.info("P110M 상태 조회 완료")
            return True
        
        elif action == "on":
            if current_state:
                logger.info("P110M이 이미 켜져 있습니다.")
                return True
            await plug.turn_on()
            await plug.update()
            logger.info("P110M 켜기 성공")
            return True
        
        elif action == "off":
            if not current_state:
                logger.info("P110M이 이미 꺼져 있습니다.")
                return True
            await plug.turn_off()
            await plug.update()
            logger.info("P110M 끄기 성공")
            return True
        
        elif action == "toggle":
            if current_state:
                await plug.turn_off()
                logger.info("P110M 끄기 (toggle)")
            else:
                await plug.turn_on()
                logger.info("P110M 켜기 (toggle)")
            await plug.update()
            return True
        
        elif action == "energy":
            if plug.has_emeter:
                energy_data = plug.emeter_realtime
                logger.info("에너지 데이터:")
                logger.info("  전력: %s W", energy_data.get("power", "N/A"))
                logger.info("  전압: %s V", energy_data.get("voltage", "N/A"))
                logger.info("  전류: %s A", energy_data.get("current", "N/A"))
                logger.info("  총 에너지: %s kWh", energy_data.get("total", "N/A"))
                return True
            else:
                logger.warning("이 장치는 에너지 모니터링을 지원하지 않습니다.")
                return False
        
        else:
            logger.error("지원하지 않는 액션입니다: %s", action)
            return False
            
    except Exception as e:
        logger.error("P110M 제어 중 예외 발생: %s", e, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_pk_p110m_controlled_via_python_kasa_library(
    action: str,
    *,
    host: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    discover: bool = True,
) -> bool:
    """
    Tapo 로컬 API (python-kasa)를 통해 P110M을 직접 제어합니다.
    
    Home Assistant 없이 로컬 네트워크에서 직접 제어합니다.
    Xavier를 통해 제어하므로 Xavier가 P110M과 같은 네트워크에 있어야 합니다.
    
    :param action: 제어 액션 ("on", "off", "toggle", "status", "energy")
    :param host: P110M의 IP 주소 (None인 경우 환경변수 또는 입력받기)
    :param username: 사용하지 않음 (python-kasa는 로컬 제어이므로 계정 불필요)
    :param password: 사용하지 않음 (python-kasa는 로컬 제어이므로 계정 불필요)
    :param discover: IP가 없을 때 자동 발견 시도 여부
    :return: 제어 성공 여부
    """
    if action not in ("on", "off", "toggle", "status", "energy"):
        logger.error("지원하지 않는 액션입니다: %s (지원: on, off, toggle, status, energy)", action)
        return False
    
    # P110M IP 주소 확인
    func_n = get_caller_name()
    
    if not host:
        host = ensure_env_var_completed_2025_11_24(
            key_name="P110M_HOST",
            func_n=func_n,
            guide_text="P110M의 IP 주소를 입력하세요 (예: 192.168.0.15):",
        )
    
    if not host:
        logger.error("P110M IP 주소가 입력되지 않았습니다.")
        return False
    
    # Xavier를 통해 P110M 제어 (Xavier가 P110M과 같은 네트워크에 있어야 함)
    logger.info("Xavier를 통해 P110M 제어 시작 (python-kasa): action=%s, host=%s", action, host)
    
    try:
        from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
            PkWirelessTargetController,
        )
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_operation_options import (
            SetupOpsForPkWirelessTargetController,
        )
        
        global _cached_controller, _connection_verified, _cached_p110m_host
        
        # 같은 세션에서 controller 재사용
        if _cached_controller is None:
            logger.info("Xavier 연결 생성 중...")
            _cached_controller = PkWirelessTargetController(
                identifier=PkDevice.jetson_agx_xavier,
                setup_op=SetupOpsForPkWirelessTargetController.TARGET,
            )
        else:
            logger.info("✅ 기존 Xavier 연결 재사용")
        
        controller = _cached_controller
        
        # 같은 P110M 호스트에 대한 연결 확인은 한 번만 수행
        if not _connection_verified or _cached_p110m_host != host:
            logger.info("Xavier에서 P110M 연결 테스트 중...")
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd=f"ping -c 2 {host}",
                timeout_seconds=10,
                use_sudo=False,
            )
            
            if exit_code != 0:
                logger.warning("Xavier에서 P110M으로 ping 실패. 네트워크 연결을 확인하세요.")
                logger.info("Xavier를 P110M과 같은 Wi-Fi 네트워크에 연결하세요.")
                _connection_verified = False
                _cached_p110m_host = None
            else:
                logger.info("✅ Xavier에서 P110M 연결 확인됨")
                _connection_verified = True
                _cached_p110m_host = host
        else:
            logger.info("✅ P110M 연결 확인 상태 재사용 (이미 확인됨)")
        
        # Xavier에 python-kasa 라이브러리 설치 확인
        logger.info("Xavier에 python-kasa 라이브러리 설치 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd="python3 -c 'import kasa; print(\"kasa installed\")'",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code != 0:
            logger.info("Xavier에 python-kasa 라이브러리 설치 중...")
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd="python3 -m pip install python-kasa",
                timeout_seconds=120,
                use_sudo=False,
            )
            
            if exit_code != 0:
                logger.error("Xavier에 python-kasa 라이브러리 설치 실패")
                return False
            logger.info("✅ Xavier에 python-kasa 라이브러리 설치 완료")
        else:
            logger.info("✅ Xavier에 python-kasa 라이브러리 이미 설치됨")
        
        # Xavier에서 실행할 Python 스크립트 생성
        import tempfile
        import textwrap
        import json
        
        host_escaped = json.dumps(host)
        action_escaped = json.dumps(action)
        
        script_content = textwrap.dedent(f"""
import asyncio
import sys
from kasa import SmartPlug

async def control_p110m():
    host = {host_escaped}
    action = {action_escaped}
    
    # python-kasa는 기본적으로 포트 9999를 사용하지만, Tapo 장치는 다른 포트를 사용할 수 있음
    # python-kasa는 Tapo 장치를 완전히 지원하지 않을 수 있음
    plug = None
    last_error = None
    
    # 기본 포트 (9999)로 시도
    try:
        print("기본 포트(9999)로 연결 시도 중...", file=sys.stderr)
        plug = SmartPlug(host)
        await plug.update()
        print("기본 포트로 연결 성공!", file=sys.stderr)
    except Exception as e:
        last_error = e
        print(f"기본 포트 연결 실패: {{e}}", file=sys.stderr)
        # python-kasa는 포트를 변경할 수 없으므로, 여기서 중단
    
    if plug is None:
        error_str = str(last_error) if last_error is not None else "연결 실패"
        print(f"오류 발생: {{error_str}}", file=sys.stderr)
        print("", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("네트워크 연결 실패", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"P110M ({{host}})에 연결할 수 없습니다.", file=sys.stderr)
        print("", file=sys.stderr)
        print("시도한 포트: 9999 (python-kasa 기본 포트)", file=sys.stderr)
        print("", file=sys.stderr)
        print("가능한 원인:", file=sys.stderr)
        print("  1. python-kasa는 Tapo 장치를 완전히 지원하지 않을 수 있습니다.", file=sys.stderr)
        print("     - python-kasa는 주로 Kasa 장치용이며, Tapo 장치는 다른 프로토콜을 사용할 수 있습니다.", file=sys.stderr)
        print("  2. Xavier와 P110M이 다른 네트워크에 있습니다.", file=sys.stderr)
        print("  3. P110M의 IP 주소가 잘못되었습니다.", file=sys.stderr)
        print("  4. P110M이 꺼져 있거나 네트워크에 연결되지 않았습니다.", file=sys.stderr)
        print("  5. P110M이 로컬 제어를 지원하지 않거나 비활성화되어 있습니다.", file=sys.stderr)
        print("", file=sys.stderr)
        print("해결 방법 (권장 순서):", file=sys.stderr)
        print("  1. Home Assistant를 통한 제어를 사용하세요 (가장 안정적):", file=sys.stderr)
        print("     - 'P110M control via Home Assistant' 작업을 사용하세요", file=sys.stderr)
        print("  2. tapo 라이브러리를 사용하세요:", file=sys.stderr)
        print("     - 'P110M control via Tapo Library (tapo)' 작업을 사용하세요", file=sys.stderr)
        print("  3. Xavier를 P110M과 같은 Wi-Fi 네트워크에 연결하세요:", file=sys.stderr)
        print("     - 'Xavier Wi-Fi 네트워크 연결' 작업을 사용하세요", file=sys.stderr)
        print("  4. P110M의 IP 주소를 확인하세요:", file=sys.stderr)
        print("     - Tapo 앱에서 장치 정보 확인", file=sys.stderr)
        print("     - 라우터 관리 페이지에서 연결된 장치 확인", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        sys.exit(1)
    
    try:
        
        current_state = plug.is_on
        print(f"P110M 현재 상태: {{'ON' if current_state else 'OFF'}}")
        
        if action == "status":
            print("P110M 상태 조회 완료")
            if plug.has_emeter:
                emeter = plug.emeter_realtime
                print(f"  전력: {{emeter.get('power', 'N/A')}} W")
                print(f"  전압: {{emeter.get('voltage', 'N/A')}} V")
                print(f"  전류: {{emeter.get('current', 'N/A')}} A")
                print(f"  총 에너지: {{emeter.get('total', 'N/A')}} kWh")
        elif action == "on":
            if current_state:
                print("P110M이 이미 켜져 있습니다.")
            else:
                await plug.turn_on()
                await plug.update()
                print("P110M 켜기 성공")
        elif action == "off":
            if not current_state:
                print("P110M이 이미 꺼져 있습니다.")
            else:
                await plug.turn_off()
                await plug.update()
                print("P110M 끄기 성공")
        elif action == "toggle":
            if current_state:
                await plug.turn_off()
                print("P110M 끄기 (toggle)")
            else:
                await plug.turn_on()
                print("P110M 켜기 (toggle)")
            await plug.update()
        elif action == "energy":
            if plug.has_emeter:
                emeter = plug.emeter_realtime
                print(f"전력: {{emeter.get('power', 'N/A')}} W")
                print(f"전압: {{emeter.get('voltage', 'N/A')}} V")
                print(f"전류: {{emeter.get('current', 'N/A')}} A")
                print(f"총 에너지: {{emeter.get('total', 'N/A')}} kWh")
            else:
                print("이 장치는 에너지 모니터링을 지원하지 않습니다.", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"지원하지 않는 액션: {{action}}", file=sys.stderr)
            sys.exit(1)
        
        sys.exit(0)
    except Exception as e:
        error_str = str(e)
        print(f"오류 발생: {{error_str}}", file=sys.stderr)
        
        # 네트워크 연결 오류인 경우 상세 정보 제공
        if "Connect" in error_str or "연결" in error_str or "timeout" in error_str.lower():
            print("", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
            print("네트워크 연결 실패", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
            print(f"P110M ({{host}})에 연결할 수 없습니다.", file=sys.stderr)
            print("", file=sys.stderr)
            print("가능한 원인:", file=sys.stderr)
            print("  1. Xavier와 P110M이 다른 네트워크에 있습니다.", file=sys.stderr)
            print("  2. P110M의 IP 주소가 잘못되었습니다.", file=sys.stderr)
            print("  3. P110M이 꺼져 있거나 네트워크에 연결되지 않았습니다.", file=sys.stderr)
            print("", file=sys.stderr)
            print("해결 방법:", file=sys.stderr)
            print("  1. Xavier를 P110M과 같은 Wi-Fi 네트워크에 연결하세요:", file=sys.stderr)
            print("     - 'Xavier Wi-Fi 네트워크 연결' 작업을 사용하세요", file=sys.stderr)
            print("  2. P110M의 IP 주소를 확인하세요:", file=sys.stderr)
            print("     - Tapo 앱에서 장치 정보 확인", file=sys.stderr)
            print("     - 라우터 관리 페이지에서 연결된 장치 확인", file=sys.stderr)
            print("  3. 또는 Home Assistant를 통한 제어를 사용하세요:", file=sys.stderr)
            print("     - 'P110M control via Home Assistant' 작업을 사용하세요", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
        
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(control_p110m())
""")
        
        # 임시 스크립트 파일 생성
        temp_script_path = None
        remote_script_path = "/tmp/ensure_pk_p110m_controlled_via_python_kasa_library.py"
        
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                suffix=".py",
                encoding="utf-8",
            ) as temp_f:
                temp_script_path = temp_f.name
                temp_f.write(script_content)
            
            # Xavier에 스크립트 전송
            logger.info("P110M 제어 스크립트를 Xavier에 전송 중...")
            ok = controller.ensure_file_transferred_to_target(
                temp_script_path,
                remote_script_path,
            )
            
            if not ok:
                logger.error("스크립트 전송 실패")
                return False
            
            # Xavier에서 스크립트 실행
            logger.info("Xavier에서 P110M 제어 스크립트 실행 중...")
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd=f"python3 {remote_script_path}",
                timeout_seconds=30,
                use_sudo=False,
            )
            
            if exit_code == 0:
                logger.info("✅ P110M 제어 성공: %s", action)
                if stdout:
                    for line in stdout:
                        logger.info("  %s", line)
                return True
            else:
                logger.error("P110M 제어 실패: %s", action)
                if stderr:
                    for line in stderr:
                        logger.error("  %s", line)
                return False
                
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception:
                    pass
        
    except Exception as e:
        logger.error("Xavier를 통한 P110M 제어 중 예외 발생: %s", e, exc_info=True)
        return False


@ensure_seconds_measured
def get_p110m_energy_data_via_tapo_local(
    *,
    host: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Tapo 로컬 API를 통해 P110M의 에너지 데이터를 조회합니다.
    
    :param host: P110M의 IP 주소
    :param username: Tapo 계정 이메일
    :param password: Tapo 계정 비밀번호
    :return: 에너지 데이터 딕셔너리 또는 None
        형식: {
            "power": float,  # 전력 (W)
            "voltage": float,  # 전압 (V)
            "current": float,  # 전류 (A)
            "total": float,  # 총 에너지 (kWh)
        }
    """
    try:
        success = ensure_pk_p110m_controlled_via_python_kasa_library(
            action="energy",
            host=host,
            username=username,
            password=password,
            discover=True,
        )
        
        if not success:
            return None
        
        # 에너지 데이터는 로그에 출력되므로, 실제로는 함수 내부에서 반환하도록 수정 필요
        # 여기서는 간단히 성공 여부만 반환
        return {"status": "success"}
        
    except Exception as e:
        logger.error("에너지 데이터 조회 중 예외 발생: %s", e, exc_info=True)
        return None


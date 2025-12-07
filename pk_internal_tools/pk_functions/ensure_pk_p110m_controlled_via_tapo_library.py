#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tapo 라이브러리를 통해 P110M을 제어하는 함수.

Xavier를 통해 tapo 라이브러리를 사용하여 P110M을 제어합니다.
Tapo 계정 인증이 필요합니다.

참고:
- tapo: https://pypi.org/project/tapo/
"""
import json
import logging
import os
import tempfile
from typing import Optional

from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
    ensure_env_var_completed_2025_11_24,
)
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import d_pk_remote_scripts

logger = logging.getLogger(__name__)

# 모듈 레벨 변수: 같은 세션에서 controller와 연결 상태를 재사용
_cached_controller = None
_connection_verified = False
_cached_p110m_host = None


@ensure_seconds_measured
def ensure_pk_p110m_controlled_via_tapo_library(
        action: str,
        *,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
) -> bool:
    """
    Tapo 라이브러리를 통해 P110M을 제어합니다.
    
    Xavier를 통해 tapo 라이브러리를 사용하여 P110M을 제어합니다.
    Tapo 계정 인증이 필요합니다.
    
    :param action: 제어 액션 ("on", "off", "toggle", "info")
    :param host: P110M의 IP 주소 (None인 경우 환경변수 또는 입력받기)
    :param username: Tapo 계정 이메일 (None인 경우 환경변수 또는 입력받기)
    :param password: Tapo 계정 비밀번호 (None인 경우 환경변수 또는 입력받기)
    :return: 제어 성공 여부
    """
    if action not in ("on", "off", "toggle", "info"):
        logger.error(f"지원하지 않는 액션입니다: {action} (지원: on, off, toggle, info)")
        return False

    # P110M IP 주소, Tapo 계정 정보 확인
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

    if not username:
        username = ensure_env_var_completed_2025_11_24(
            key_name="TAPO_USERNAME",
            func_n=func_n,
            guide_text="Tapo 계정 이메일을 입력하세요:",
        )

    if not username:
        logger.error("Tapo 계정 이메일이 입력되지 않았습니다.")
        return False

    if not password:
        password = ensure_env_var_completed_2025_11_24(
            key_name="TAPO_PW",
            func_n=func_n,
            guide_text="Tapo 계정 비밀번호를 입력하세요:",
        )

    if not password:
        logger.error("Tapo 계정 비밀번호가 입력되지 않았습니다.")
        return False

    # Xavier를 통해 P110M 제어 (Xavier가 P110M과 같은 네트워크에 있어야 함)
    logger.info(f"Xavier를 통해 P110M 제어 시작 (tapo): action={action}, host={host}")

    try:
        from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
            PkWirelessTargetController,
        )
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_operation_options import (
            SetupOpsForPkWirelessTargetController,
        )
        from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
        from pk_internal_tools.pk_objects.pk_directories import (
            d_pk_internal_tools,
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

        # Xavier에 tapo 라이브러리 설치 확인
        logger.info("Xavier에 tapo 라이브러리 설치 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd="python3 -c 'import tapo; print(\"tapo installed\")'",
            timeout_seconds=10,
            use_sudo=False,
        )

        if exit_code != 0:
            logger.info("Xavier에 tapo 라이브러리 설치 중...")
            stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                cmd="python3 -m pip install tapo",
                timeout_seconds=120,
                use_sudo=False,
            )

            if exit_code != 0:
                logger.error("Xavier에 tapo 라이브러리 설치 실패")
                return False
            logger.info("✅ Xavier에 tapo 라이브러리 설치 완료")
        else:
            logger.info("✅ Xavier에 tapo 라이브러리 이미 설치됨")

        # Remote script 템플릿 파일 읽기
        remote_script_template_file = d_pk_remote_scripts / "ensure_pk_p110m_controlled_via_tapo_library_remote.py"
        remote_script_template = get_str_from_f(f=str(remote_script_template_file))

        if not remote_script_template:
            logger.error(f"remote script template file is not readable: {remote_script_template_file}")
            return False

        # 플레이스홀더 치환
        host_escaped = json.dumps(host)
        username_escaped = json.dumps(username)
        password_escaped = json.dumps(password)
        action_escaped = json.dumps(action)

        remote_script = remote_script_template.replace("{HOST_ESCAPED}", host_escaped)
        remote_script = remote_script.replace("{USERNAME_ESCAPED}", username_escaped)
        remote_script = remote_script.replace("{PASSWORD_ESCAPED}", password_escaped)
        remote_script = remote_script.replace("{ACTION_ESCAPED}", action_escaped)

        # 임시 스크립트 파일 생성
        temp_script_path = None
        remote_script_path = "/tmp/ensure_pk_p110m_controlled_via_tapo_library.py"

        try:
            with tempfile.NamedTemporaryFile(
                    mode="w",
                    delete=False,
                    suffix=".py",
                    encoding="utf-8",
            ) as temp_f:
                temp_script_path = temp_f.name
                temp_f.write(remote_script)

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
                timeout_seconds=60,
                use_sudo=False,
            )

            if exit_code == 0:
                logger.info(f"✅ P110M 제어 성공: {action}")

                # stdout/stderr 출력 (info 액션인 경우 노란색으로 출력)
                if action == "info":
                    from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
                    if stdout:
                        for line in stdout:
                            print(get_text_yellow(line))
                    if stderr:
                        for line in stderr:
                            print(get_text_yellow(line))

                    # 호스트 머신에서 사용자 입력 대기
                    print("")
                    print("=" * 60)
                    input("continue:enter")
                else:
                    # 다른 액션은 기존대로 로그 출력
                    if stdout:
                        for line in stdout:
                            logger.info(f"  {line}")
                    if stderr:
                        for line in stderr:
                            logger.info(f"  {line}")

                return True
            else:
                logger.error(f"P110M 제어 실패: {action}")
                if stderr:
                    for line in stderr:
                        logger.error(f"  {line}")
                return False

        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception:
                    pass

    except Exception as e:
        logger.error(f"Xavier를 통한 P110M 제어 중 예외 발생: {e}", exc_info=True)
        return False

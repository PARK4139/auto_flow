#!/usr/bin/env python3

"""
Xavier에 Arduino 개발 환경을 온보딩하는 함수

VSCode + PlatformIO + platformio.ini 기반으로 Arduino 및 개발 보드 개발 환경을 설정합니다.
"""
import logging
from typing import Optional

from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)

logger = logging.getLogger(__name__)


def ensure_arduino_dev_environment_onboarded_on_remote_target(
        remote_target_ip: Optional[str] = None,
        remote_target_user: Optional[str] = None,
        remote_target_pw: Optional[str] = None,
) -> bool:
    """
    Xavier에 Arduino 개발 환경을 온보딩합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        
    Returns:
        bool: 온보딩 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed

        # remote_target 연결 정보 가져오기
        if not remote_target_ip:
            remote_target_ip = ensure_env_var_completed("XAVIER_IP")
        if not remote_target_user:
            remote_target_user = ensure_env_var_completed("XAVIER_USER")
        if not remote_target_pw:
            remote_target_pw = ensure_env_var_completed("XAVIER_PW")

        # Xavier 컨트롤러 생성
        controller = PkRemoteTargetEngine(
            
            ip=remote_target_ip,
            user_n=remote_target_user,
            pw=remote_target_pw,
        )

        logger.info("=" * 60)
        logger.info("Arduino 개발 환경 온보딩 시작 (Xavier)")
        logger.info("=" * 60)

        # 1. 필수 패키지 설치
        logger.info("1. 필수 패키지 설치 중...")
        packages_to_install = [
            "python3-pip",
            "python3-dev",
            "build-essential",
            "git",
            "udev",
        ]

        for package in packages_to_install:
            logger.info("  - %s 설치 중...", package)
            cmd = f"sudo apt-get update && sudo apt-get install -y {package}"
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd=cmd,
                timeout_seconds=120,
                use_sudo=False,
            )
            if exit_code != 0:
                logger.warning("  ⚠️ %s 설치 실패 (계속 진행)", package)
                if stderr:
                    for line in stderr:
                        logger.debug("    %s", line)

        # 2. PlatformIO 설치
        logger.info("2. PlatformIO 설치 중...")
        pio_install_commands = [
            "python3 -m pip install --user platformio",
            "python3 -m pip install --user --upgrade platformio",
        ]

        for cmd in pio_install_commands:
            logger.info("  실행: %s", cmd)
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd=cmd,
                timeout_seconds=300,
                use_sudo=False,
            )
            if exit_code == 0:
                logger.info("  ✅ PlatformIO 설치 완료")
                if stdout:
                    for line in stdout[-5:]:  # 마지막 5줄만 출력
                        logger.debug("    %s", line)
                break
            else:
                logger.warning("  ⚠️ PlatformIO 설치 실패 (재시도)")
                if stderr:
                    for line in stderr[-5:]:
                        logger.debug("    %s", line)

        # 3. PlatformIO PATH 확인 및 설정
        logger.info("3. PlatformIO PATH 설정 확인 중...")
        pio_path_cmd = "python3 -m platformio --version"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=pio_path_cmd,
            timeout_seconds=30,
            use_sudo=False,
        )

        if exit_code == 0 and stdout:
            pio_version = stdout[0].strip() if stdout else "unknown"
            logger.info("  ✅ PlatformIO 버전: %s", pio_version)
        else:
            logger.warning("  ⚠️ PlatformIO 버전 확인 실패")
            logger.info("  PATH에 ~/.local/bin 추가 필요할 수 있습니다.")

        # 4. udev 규칙 설정 (USB 시리얼 장치 접근 권한)
        logger.info("4. USB 시리얼 장치 접근 권한 설정 중...")
        udev_rules_content = """# Arduino and other USB-to-Serial devices
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0666", GROUP="dialout"
"""

        # udev 규칙 파일 생성
        udev_rules_path = "/tmp/99-platformio-udev.rules"
        import tempfile
        with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                suffix=".rules",
                encoding="utf-8",
        ) as temp_f:
            temp_rules_path = temp_f.name
            temp_f.write(udev_rules_content)

        try:
            # Xavier에 udev 규칙 파일 전송
            remote_rules_path = "/tmp/99-platformio-udev.rules"
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_rules_path,
                remote_rules_path,
            )

            if ok:
                # udev 규칙 설치
                install_udev_cmd = f"sudo cp {remote_rules_path} /etc/udev/rules.d/ && sudo udevadm control --reload-rules && sudo udevadm trigger"
                stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                    cmd=install_udev_cmd,
                    timeout_seconds=30,
                    use_sudo=False,
                )

                if exit_code == 0:
                    logger.info("  ✅ udev 규칙 설치 완료")
                else:
                    logger.warning("  ⚠️ udev 규칙 설치 실패")
            else:
                logger.warning("  ⚠️ udev 규칙 파일 전송 실패")
        finally:
            import os
            if temp_rules_path and os.path.exists(temp_rules_path):
                try:
                    os.remove(temp_rules_path)
                except Exception as e:
                    pass

        # 5. 사용자를 dialout 그룹에 추가 (USB 시리얼 접근 권한)
        logger.info("5. 사용자를 dialout 그룹에 추가 중...")
        add_user_group_cmd = f"sudo usermod -a -G dialout {remote_target_user}"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=add_user_group_cmd,
            timeout_seconds=30,
            use_sudo=False,
        )

        if exit_code == 0:
            logger.info("  ✅ 사용자가 dialout 그룹에 추가되었습니다.")
            logger.info("  ⚠️ 그룹 변경사항 적용을 위해 재로그인 또는 재부팅이 필요합니다.")
        else:
            logger.warning("  ⚠️ 그룹 추가 실패")

        # 6. 기본 프로젝트 디렉토리 생성
        logger.info("6. 기본 프로젝트 디렉토리 생성 중...")
        project_dir = f"~/arduino_projects"
        create_dir_cmd = f"mkdir -p {project_dir}"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=create_dir_cmd,
            timeout_seconds=10,
            use_sudo=False,
        )

        if exit_code == 0:
            logger.info("  ✅ 프로젝트 디렉토리 생성 완료: %s", project_dir)
        else:
            logger.warning("  ⚠️ 프로젝트 디렉토리 생성 실패")

        # 7. 기본 platformio.ini 템플릿 생성
        logger.info("7. 기본 platformio.ini 템플릿 생성 중...")

        # 타겟 구성 클래스에서 platformio.ini 생성
        from pk_internal_tools.pk_objects.pk_arduino_target_config import (
            ArduinoTargetType,
            get_platformio_ini_for_target,
            get_all_target_types,
            get_arduino_target_config,
        )

        # 기본 타겟: Arduino Nano + ESP8266 + esp-link
        default_target = ArduinoTargetType.NANO_ESP8266_ESPLINK
        default_config = get_arduino_target_config(default_target)

        # platformio.ini 템플릿 생성
        platformio_ini_template = f"""[platformio]
default_envs = {default_config.platformio_env}

# 기본 타겟: {default_config.description}
{get_platformio_ini_for_target(default_target)}

# 다른 보드 환경 (확장용)
"""

        # 모든 타겟 타입에 대한 환경 추가
        for target_type in get_all_target_types():
            if target_type != default_target:
                config = get_arduino_target_config(target_type)
                if config:
                    platformio_ini_template += f"""
# {config.description}
{get_platformio_ini_for_target(target_type)}
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
            temp_f.write(platformio_ini_template)

        try:
            # Xavier에 platformio.ini 템플릿 전송
            remote_ini_path = f"{project_dir}/platformio.ini.template"
            ok = controller.ensure_file_transferred_to_remote_target(
                temp_ini_path,
                remote_ini_path,
            )

            if ok:
                logger.info("  ✅ platformio.ini 템플릿 생성 완료: %s", remote_ini_path)
            else:
                logger.warning("  ⚠️ platformio.ini 템플릿 생성 실패")
        finally:
            import os
            if temp_ini_path and os.path.exists(temp_ini_path):
                try:
                    os.remove(temp_ini_path)
                except Exception as e:
                    pass

        # 8. VSCode Remote SSH 설정 안내
        logger.info("=" * 60)
        logger.info("✅ Arduino 개발 환경 온보딩 완료")
        logger.info("=" * 60)
        logger.info("")
        logger.info("다음 단계:")
        logger.info("1. VSCode에서 Remote-SSH 확장 설치 (이미 설치되어 있을 수 있음)")
        logger.info("2. VSCode에서 F1 > 'Remote-SSH: Connect to Host' 선택")
        logger.info("3. '%s@%s' 입력", remote_target_user, remote_target_ip)
        logger.info("4. 연결 후 PlatformIO 확장 설치")
        logger.info("5. 프로젝트 디렉토리 열기: %s", project_dir)
        logger.info("6. platformio.ini.template을 복사하여 새 프로젝트 생성")
        logger.info("")
        logger.info("참고:")
        logger.info("- USB 시리얼 장치 접근 권한을 위해 재로그인 또는 재부팅이 필요할 수 있습니다.")
        logger.info("- PlatformIO 명령어: python3 -m platformio")
        logger.info("- PlatformIO PATH: ~/.local/bin (필요시 .bashrc에 추가)")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("Arduino 개발 환경 온보딩 중 예외 발생: %s", e, exc_info=True)
        return False

import logging
import time
from typing import Optional


def ensure_home_assistant_ready_on_target(
    target_controller,
    *,
    container_name: str = "homeassistant",
    config_dir: str = "/opt/homeassistant",
    image_ref: str = "ghcr.io/home-assistant/home-assistant:stable",
) -> bool:
    """
    타겟 장치(Xavier 등)에서 Home Assistant Docker 컨테이너가 설치·실행 중인지 확인하고,
    없으면 자동으로 설치 및 기동합니다.

    1) docker 컨테이너 상태 확인
    2) 필요 시 docker 설치 (target_controller.ensure_remote_target_distro_docker_installed 활용)
    3) 설정 디렉터리 생성 및 권한 조정
    4) Home Assistant 컨테이너 실행
    5) HTTP Health 체크 (http://localhost:8123)
    """

    def _run(cmd: str, *, desc: str, use_sudo: bool = True, timeout: int = 120):
        logging.debug("[ensure-ha] 실행 준비 (%s): %s", desc, cmd)
        stdout, stderr, exit_status = target_controller.ensure_command_to_remote_target(
            cmd=cmd,
            timeout_seconds=timeout,
            use_sudo=use_sudo,
        )
        logging.debug(
            "[ensure-ha] 실행 완료 (%s)\n"
            "  - exit_status: %s\n"
            "  - stdout: %s\n"
            "  - stderr: %s",
            desc,
            exit_status,
            stdout if stdout else "<empty>",
            stderr if stderr else "<empty>",
        )
        return stdout, stderr, exit_status

    def _is_container_running() -> bool:
        stdout, _, exit_status = _run(
            cmd=f"docker ps --filter name={container_name} --format '{{{{.Names}}}}'",
            desc="컨테이너 상태 확인",
            use_sudo=True,
            timeout=30,
        )
        if exit_status == 0 and stdout:
            running = container_name in stdout[0]
            if running:
                logging.info("Home Assistant 컨테이너가 이미 실행 중입니다.")
            return running
        return False

    def _wait_for_http_ready(retries: int = 10, delay: int = 6) -> bool:
        check_cmd = (
            "python3 -c \"import urllib.request,sys;url='http://localhost:8123';"
            "req=urllib.request.Request(url);"
            "import urllib.error;"
            "import socket;"
            "try:\\n"
            "    urllib.request.urlopen(req, timeout=5)\\n"
            "    ;sys.exit(0)\\n"
            "except Exception as exc:\\n"
            "    print(exc)\\n"
            "    ;sys.exit(1)\""
        )

        for attempt in range(1, retries + 1):
            stdout, _, exit_status = _run(
                cmd=check_cmd,
                desc=f"Home Assistant HTTP 응답 확인 (시도 {attempt}/{retries})",
                use_sudo=False,
                timeout=20,
            )
            if exit_status == 0:
                logging.info("Home Assistant HTTP 응답이 확인되었습니다.")
                return True
            logging.debug(
                "Home Assistant HTTP 확인 실패 (attempt=%s, stdout=%s). %s초 후 재시도합니다.",
                attempt,
                stdout,
                delay,
            )
            time.sleep(delay)
        logging.error("Home Assistant HTTP 확인에 실패했습니다.")
        return False

    logging.info("타겟 장치에서 Home Assistant 준비 상태를 확인합니다.")

    # n. 이미 실행 중인지 확인
    if _is_container_running():
        return True

    # 2) docker 설치 보장
    try:
        logging.info("Docker 설치 및 구성을 확인합니다.")
        target_controller.ensure_remote_target_distro_docker_installed()
    except Exception as docker_error:
        logging.error("Docker 설치/구성 중 오류 발생: %s", docker_error)
        return False

    # 3) 설정 디렉터리 생성
    target_user = getattr(target_controller.remote_target, "user_name", "pk")
    _run(
        cmd=f"mkdir -p {config_dir} && chown -R {target_user}:{target_user} {config_dir}",
        desc="Home Assistant 설정 디렉터리 준비",
        use_sudo=True,
    )

    # 4) 기존 컨테이너 제거
    _run(
        cmd=f"docker rm -f {container_name} || true",
        desc="이전 Home Assistant 컨테이너 제거",
        use_sudo=True,
    )

    # 5) 컨테이너 실행
    run_cmd = (
        f"docker run -d --name {container_name} "
        "--restart unless-stopped --privileged "
        "-p 8123:8123 "
        f"-v {config_dir}:/config "
        "-e TZ=Asia/Seoul "
        f"{image_ref}"
    )
    stdout, stderr, exit_status = _run(
        cmd=run_cmd,
        desc="Home Assistant 컨테이너 실행",
        use_sudo=True,
        timeout=180,
    )
    if exit_status != 0:
        logging.error("Home Assistant 컨테이너 실행에 실패했습니다.")
        return False

    # 6) 컨테이너 가동 대기 및 확인
    if not _is_container_running():
        logging.info("컨테이너 기동을 기다립니다.")
        for attempt in range(1, 11):
            if _is_container_running():
                break
            logging.debug("컨테이너 기동 대기 중... (%s/10)", attempt)
            time.sleep(5)
        else:
            logging.error("Home Assistant 컨테이너가 시작되지 않았습니다.")
            return False

    # 7) HTTP health 확인
    return _wait_for_http_ready()



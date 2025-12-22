#!/usr/bin/env python3

"""
LG TV 제어 함수 (Xavier > LG think Q > TV ON/OFF)
Home Assistant를 통해 LG TV를 제어합니다.

동작구현 어려우면 Xavier > 스마트 플러그 > TV ON/OFF 안전 검토 후 안전하면 구현
"""
import logging
import os
import re
import tempfile
import textwrap
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine

logger = logging.getLogger(__name__)


class PkTvController:
    """
    Controller that asks the target device (Jetson Xavier) to call Home Assistant REST API
    and control an LG TV via its HA media_player entity.

    - Assumes Home Assistant is running on the target (Xavier) at http://localhost:8123
      by default (can be overridden).
    - Authentication is done via Home Assistant Long-Lived Access Token.
      Token can be passed via argument or set on the target as env var HA_TOKEN.
    """

    def __init__(
        self,
        remote_target_controller: "PkRemoteTargetEngine",
        ha_url: Optional[str] = None,
        ha_token_env_name: str = "HA_TOKEN",
    ) -> None:
        self.target_controller = remote_target_controller
        self._target = self.target_controller.remote_target  # for convenience
        target_ip = getattr(self._target, "ip", None) or getattr(self._target, "hostname", None)
        default_ha_url = f"http://{target_ip}:8123" if target_ip else "http://localhost:8123"
        self.ha_url = ha_url or default_ha_url
        if target_ip:
            logging.debug("Home Assistant 기본 URL을 타겟 IP 기반으로 설정했습니다: %s", self.ha_url)
        else:
            logging.debug("타겟 IP를 확인할 수 없어 localhost 기본 URL을 사용합니다: %s", self.ha_url)
        self.ha_token_env_name = ha_token_env_name

    # -------------------------------------------------------------------------
    # Internal: script content to be executed on the target (Xavier)
    # -------------------------------------------------------------------------
    def _get_tv_control_script_content(self) -> str:
        """
        Returns Python script content that will run on the target (Xavier).
        The script will:
          - parse arguments (action/entity/ha-url/ha-token)
          - call Home Assistant REST API to control the given media_player entity (TV)
        """
        script_content = """
import argparse
import logging
import os
import sys
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def call_ha_media_player(action: str, entity_id: str, ha_url: str, ha_token: str) -> bool:
    # Call Home Assistant media_player service to control TV.
    # action: "on", "off", "toggle"
    # entity_id: media_player entity ID (e.g., media_player.lg_tv)
    if action not in ("on", "off", "toggle"):
        logging.error("Unsupported action: %s", action)
        return False

    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    # handle toggle by reading current state first
    if action == "toggle":
        state_url = ha_url.rstrip("/") + f"/api/states/{entity_id}"
        try:
            resp = requests.get(state_url, headers=headers, timeout=5)
        except Exception as e:
            logging.error("Exception while getting current state: %s", e)
            return False

        if resp.status_code // 100 != 2:
            logging.error("Failed to get current state: %s %s", resp.status_code, resp.text)
            return False

        cur_state = resp.json().get("state")
        # For media_player, "on" means on, "off" or "standby" means off
        if cur_state in ("on", "playing", "paused"):
            next_action = "off"
        else:
            next_action = "on"
        logging.info("Current state: %s -> switching to %s", cur_state, next_action)
        action = next_action

    # Call media_player service
    if action == "on":
        service_name = "turn_on"
        service_domain = "media_player"
    elif action == "off":
        # LG TV의 경우 media_player.turn_off가 동작하지 않을 수 있으므로
        # remote.send_command를 시도하거나 media_player.turn_off를 먼저 시도
        service_name = "turn_off"
        service_domain = "media_player"
    else:
        logging.error("Unsupported action: %s", action)
        return False

    service_url = ha_url.rstrip("/") + f"/api/services/{service_domain}/{service_name}"

    try:
        resp = requests.post(
            service_url,
            headers=headers,
            json={"entity_id": entity_id},
            timeout=10,  # TV control may take longer
        )
    except Exception as e:
        logging.error("Exception while calling Home Assistant service: %s", e)
        return False

    if resp.status_code // 100 == 2:
        logging.info("Home Assistant service call successful: %s %s", action, entity_id)
        return True

    # OFF 액션 실패 시 remote.send_command로 재시도 (LG TV용)
    if action == "off" and service_domain == "media_player":
        logging.warning("media_player.turn_off 실패, remote.send_command로 재시도합니다.")
        # remote 엔티티 찾기 (media_player.lg_tv -> remote.lg_tv)
        remote_entity_id = entity_id.replace("media_player.", "remote.")
        remote_service_url = ha_url.rstrip("/") + "/api/services/remote/send_command"
        
        try:
            # LG TV 전원 끄기 명령 (일반적인 IR 코드)
            remote_resp = requests.post(
                remote_service_url,
                headers=headers,
                json={
                    "entity_id": remote_entity_id,
                    "command": "KEY_POWER"
                },
                timeout=10,
            )
            if remote_resp.status_code // 100 == 2:
                logging.info("remote.send_command로 TV OFF 성공: %s", remote_entity_id)
                return True
            else:
                logging.warning("remote.send_command도 실패: %s %s", remote_resp.status_code, remote_resp.text)
        except Exception as e:
            logging.warning("remote.send_command 시도 중 예외: %s", e)

    logging.error(
        "Home Assistant service call failed: %s %s -> %s %s",
        action, entity_id, resp.status_code, resp.text
    )
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="LG TV via Home Assistant REST")
    parser.add_argument("--action", choices=["on", "off", "toggle"], required=True)
    parser.add_argument(
        "--entity",
        default=os.environ.get("HA_TV_ENTITY", "media_player.lg_tv"),
        help="Target HA media_player entity_id",
    )
    parser.add_argument(
        "--ha-url",
        default=os.environ.get("HA_URL", "http://localhost:8123"),
        help="Home Assistant base URL (e.g. http://localhost:8123)",
    )
    parser.add_argument(
        "--ha-token",
        default=os.environ.get("HA_TOKEN"),
        help="Home Assistant long lived access token",
    )
    args = parser.parse_args()

    if not args.ha_token:
        logging.error("HA_TOKEN (env or --ha-token) is not set.")
        return 1

    ok = call_ha_media_player(
        action=args.action,
        entity_id=args.entity,
        ha_url=args.ha_url,
        ha_token=args.ha_token,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
"""
        return textwrap.dedent(script_content)

    # -------------------------------------------------------------------------
    # Public: main entry point from pk_system
    # -------------------------------------------------------------------------
    def ensure_tv_controlled_on_target(
        self,
        action: str,
        entity_id: str,
        ha_url: Optional[str] = None,
        ha_token: Optional[str] = None,
    ) -> bool:
        """
        Ask the target (Xavier) to control TV via its Home Assistant entity.

        :param action: "on", "off", or "toggle"
        :param entity_id: HA media_player entity_id (e.g. "media_player.lg_tv")
        :param ha_url: Home Assistant base URL. If None, uses self.ha_url.
        :param ha_token: HA Long-Lived Access Token.
                         If None, script will rely on env HA_TOKEN on target.
        """
        ha_url = ha_url or self.ha_url

        script_file_name = "ensure_tv_controlled_on_target.py"
        remote_script_path = f"/tmp/{script_file_name}"

        script_content = self._get_tv_control_script_content()
        temp_script_path = None

        try:
            # n. create temp script locally
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                suffix=".py",
                encoding="utf-8",
            ) as temp_f:
                temp_script_path = temp_f.name
                temp_f.write(script_content)

            # 2) transfer to target
            logging.info(
                "TV 제어 스크립트를 타겟 장치에 전송합니다: %s",
                remote_script_path,
            )
            ok = self.target_controller.ensure_file_transferred_to_remote_target(
                temp_script_path,
                remote_script_path,
            )
            if not ok:
                logging.error("Failed to transfer control script.")
                return False
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception as e:
                    pass

        # 3) ensure 'requests' is available on target
        if not self.target_controller.ensure_requests_module_available():
            logging.error("Failed to install 'requests' on target device.")
            return False

        # 4) build remote command
        # HA_TOKEN은 환경변수로 전달 (명령줄 인자로 전달하면 특수문자 문제 발생 가능)
        cmd = f"python3 {remote_script_path} --action {action} --entity {entity_id} --ha-url '{ha_url}'"
        
        # 환경변수로 토큰 전달 (더 안전함)
        if ha_token:
            # 토큰에서 제어 문자 제거 및 검증
            # 제어 문자 제거 (0x00-0x1F, 0x7F 제외하고 공백, 탭, 개행은 유지)
            cleaned_token = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', ha_token)
            if cleaned_token != ha_token:
                logging.warning("HA_TOKEN에서 제어 문자가 제거되었습니다.")
            
            # 환경변수로 전달 (명령줄 인자보다 안전)
            # 토큰에 작은따옴표가 포함될 수 있으므로 이스케이프 처리
            escaped_token = cleaned_token.replace("'", "'\"'\"'")
            cmd = f"HA_TOKEN='{escaped_token}' {cmd}"
        
        logging.info("Executing TV control command on target device (HA_TOKEN은 환경변수로 전달됨)")
        if ha_token:
            # 로그에는 토큰을 마스킹하여 출력
            cleaned_token_local = cleaned_token if 'cleaned_token' in locals() else ha_token
            masked_cmd = cmd.replace(cleaned_token_local, '***')
            logging.debug("Command: %s", masked_cmd)
        else:
            logging.debug("Command: %s", cmd)
        stdout, stderr, exit_status = self.target_controller.ensure_command_to_remote_target(
            cmd=cmd,
            use_sudo=False,
            timeout_seconds=30,  # TV 제어는 시간이 걸릴 수 있으므로 타임아웃 설정
        )
        
        if stdout:
            logging.debug("TV 제어 스크립트 출력: %s", "\n".join(stdout))

        if exit_status != 0:
            logging.error(
                "TV 제어 스크립트 실행 실패 (Exit Code: %s): %s",
                exit_status,
                stderr,
            )
            return False

        logging.info("TV control command execution completed.")
        return True



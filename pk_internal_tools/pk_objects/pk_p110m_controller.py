import logging
import os
import tempfile
import textwrap
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # type checking only import to avoid hard dependency at import time
    from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine

class PkP110mController:
    """
    Controller that asks the target device (Jetson Xavier) to call Home Assistant REST API
    and control a P110M (Matter) smart plug via its HA switch entity.

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
    def _get_p110m_control_script_content(self) -> str:
        """
        Returns Python script content that will run on the target (Xavier).
        The script will:
          - parse arguments (action/entity/ha-url/ha-token)
          - call Home Assistant REST API to control the given switch entity
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

def call_ha_switch(action: str, entity_id: str, ha_url: str, ha_token: str) -> bool:
    if action not in ("on", "off", "toggle"):
        logging.error("지원하지 않는 액션입니다: %s", action)
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
            logging.error("현재 상태 조회 중 예외 발생: %s", e)
            return False

        if resp.status_code // 100 != 2:
            logging.error("현재 상태 조회 실패: %s %s", resp.status_code, resp.text)
            return False

        cur_state = resp.json().get("state")
        next_action = "off" if cur_state == "on" else "on"
        logging.info("현재 상태: %s -> %s 로 전환", cur_state, next_action)
        action = next_action

    service_url = ha_url.rstrip("/") + f"/api/services/switch/turn_{action}"

    try:
        resp = requests.post(
            service_url,
            headers=headers,
            json={"entity_id": entity_id},
            timeout=5,
        )
    except Exception as e:
        logging.error("Home Assistant 서비스 호출 중 예외 발생: %s", e)
        return False

    if resp.status_code // 100 == 2:
        logging.info("Home Assistant 서비스 호출 성공: %s %s", action, entity_id)
        return True

    logging.error(
        "Home Assistant 서비스 호출 실패: %s %s -> %s %s",
        action, entity_id, resp.status_code, resp.text
    )
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="P110M via Home Assistant REST")
    parser.add_argument("--action", choices=["on", "off", "toggle"], required=True)
    parser.add_argument(
        "--entity",
        default=os.environ.get("HA_ENTITY", "switch.tapo_p110m_plug"),
        help="Target HA switch entity_id",
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
        logging.error("HA_TOKEN (env or --ha-token) 이 설정되어 있지 않습니다.")
        return 1

    ok = call_ha_switch(
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
    def ensure_pk_p110m_controlled_on_target(
        self,
        action: str,
        entity_id: str,
        ha_url: Optional[str] = None,
        ha_token: Optional[str] = None,
    ) -> bool:
        """
        Ask the target (Xavier) to control P110M via its Home Assistant entity.

        :param action: "on", "off", or "toggle"
        :param entity_id: HA switch entity_id (e.g. "switch.tapo_p110m_plug")
        :param ha_url: Home Assistant base URL. If None, uses self.ha_url.
        :param ha_token: HA Long-Lived Access Token.
                         If None, script will rely on env HA_TOKEN on target.
        """
        ha_url = ha_url or self.ha_url

        script_file_name = "ensure_pk_p110m_controlled_on_target.py"
        remote_script_path = f"/tmp/{script_file_name}"

        script_content = self._get_p110m_control_script_content()
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
                "P110M 제어 스크립트를 타겟 장치에 전송합니다: %s",
                remote_script_path,
            )
            ok = self.target_controller.ensure_file_transferred_to_remote_target(
                temp_script_path,
                remote_script_path,
            )
            if not ok:
                logging.error("제어 스크립트 전송에 실패했습니다.")
                return False
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except Exception as e:
                    pass

        # 3) ensure 'requests' is available on target
        if not self.target_controller.ensure_requests_module_available():
            logging.error("타겟 장치에 'requests' 설치를 실패했습니다.")
            return False

        # 4) build remote command
        cmd = f"python3 {remote_script_path} --action {action} --entity {entity_id} --ha-url '{ha_url}'"
        if ha_token:
            # note: token 에 공백이 없다는 전제
            cmd += f" --ha-token '{ha_token}'"

        logging.info("타겟 장치에서 P110M 제어 명령을 실행합니다: %s", cmd)
        _, stderr, exit_status = self.target_controller.ensure_command_to_remote_target(
            cmd=cmd,
            use_sudo=False,
        )

        if exit_status != 0:
            logging.error(
                "P110M 제어 스크립트 실행 실패 (Exit Code: %s): %s",
                exit_status,
                stderr,
            )
            return False

        logging.info("P110M 제어 명령 실행 완료.")
        return True

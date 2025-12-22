from __future__ import annotations

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

@ensure_seconds_measured
def ensure_pk_yldp06yl_controlled_via_yeelight_library(
        action: str,
        ip: str | None = None,
        *,
        port: int = 55443,
        rgb: tuple[int, int, int] | None = None,
        brightness: int | None = None,
        color_temp: int | None = None,
        transition_ms: int = 300,
) -> bool:
    """
    Control Yeelight bulb (commonly YLDP06YL) via python 'yeelight' library over LAN.

    Prerequisites:
    - LAN control(Developer Mode) must be enabled on the bulb (Yeelight app).
    - The bulb should be reachable from this machine over the local network.
    - Optional: set env var PK_YEELIGHT_YLDP06YL_IP to skip discovery.

    Supported actions:
    - "on", "off", "toggle", "info"
    - "rgb" (requires rgb=(r,g,b))
    - "brightness" (requires brightness=1..100)
    - "ct" (requires color_temp=1700..6500 typically)
    """
    import os
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import (
        ensure_pk_wrapper_exception_routine_done,
    )

    try:
        try:
            from yeelight import Bulb, discover_bulbs
        except Exception as e:
            logging.exception(
                "Failed to import 'yeelight'. Install it first: `uv add yeelight` (or `pip install yeelight`)."
            )
            return False

        normalized_action = (action or "").strip().lower()
        if not normalized_action:
            logging.error("Action is empty.")
            return False

        if not ip:
            ip = os.environ.get("PK_YEELIGHT_YLDP06YL_IP")

        # If IP is not provided, try discovery (UDP broadcast).
        chosen_port = port
        if not ip:
            logging.info("PK_YEELIGHT_YLDP06YL_IP is not set. Trying discover_bulbs() ...")
            bulbs = discover_bulbs()  # returns list of dicts: ip, port, capabilities, ...
            if not bulbs:
                logging.error(
                    "No Yeelight bulbs discovered. Ensure LAN control is enabled and UDP broadcast is allowed."
                )
                # 디버깅 강화: 구체적인 안내 추가
                logging.info("Yeelight 앱에서 해당 전구 설정으로 이동하여 'LAN 제어 모드'를 활성화해주세요.")
                logging.info("네트워크 환경에서 UDP 브로드캐스트가 허용되어 있는지 확인하거나, 방화벽 설정을 검토해주세요.")

                # IP 수동 입력 옵션 추가
                manual_ip = ensure_value_completed(
                    key_name="yeelight_bulb_ip_manual_input",
                    func_n=get_caller_name(),
                    guide_text="Yeelight 전구를 찾지 못했습니다. 전구의 IP 주소를 수동으로 입력하시겠습니까? (건너뛰려면 Enter)",
                    options=[] # fzf를 사용하지 않고 직접 입력
                )

                if manual_ip:
                    ip = manual_ip
                    logging.info(f"수동으로 입력된 IP 주소 사용: {ip}")
                else:
                    logging.warning("IP 주소 수동 입력이 건너뛰어졌습니다. Yeelight 제어를 계속할 수 없습니다.")
                    return False
            else:
                # Pick the first discovered bulb (simple default).
                chosen = bulbs[0]
            ip = chosen.get("ip")
            chosen_port = int(chosen.get("port") or port)

            caps = chosen.get("capabilities") or {}
            logging.info(f"Discovered bulb chosen: ip={ip}, port={chosen_port}, model={caps.get('model')}, name={caps.get('name')}")

        if not ip:
            logging.error("Bulb IP is still unknown. Set PK_YEELIGHT_YLDP06YL_IP or pass ip= explicitly.")
            return False

        bulb = Bulb(ip, port=chosen_port)

        # Execute action
        if normalized_action == "on":
            bulb.turn_on(duration=transition_ms)
            return True

        if normalized_action == "off":
            bulb.turn_off(duration=transition_ms)
            return True

        if normalized_action == "toggle":
            bulb.toggle()
            return True

        if normalized_action == "info":
            props = bulb.get_properties()
            logging.info(f"Yeelight properties: {props}")
            return True

        if normalized_action == "rgb":
            if not rgb or len(rgb) != 3:
                logging.error("Action 'rgb' requires rgb=(r,g,b).")
                return False
            r, g, b = rgb
            bulb.set_rgb(int(r), int(g), int(b), duration=transition_ms)
            return True

        if normalized_action == "brightness":
            if brightness is None:
                logging.error("Action 'brightness' requires brightness=1..100.")
                return False
            bulb.set_brightness(int(brightness), duration=transition_ms)
            return True

        if normalized_action in ("ct", "color_temp", "colortemp"):
            if color_temp is None:
                logging.error("Action 'ct' requires color_temp=1700..6500.")
                return False
            bulb.set_color_temp(int(color_temp), duration=transition_ms)
            return True

        logging.error(f"Unknown action: {action}")
        return False

    except Exception as e:
        logging.error(f"Yeelight control failed: {e}")
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
        return False
    except BaseException:
        ensure_debugged_verbose(traceback, e)
        return False

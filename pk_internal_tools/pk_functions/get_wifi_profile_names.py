import logging
from typing import List

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def _exec(cmd: str) -> List[str]:
    stdout_lines, _, _ = ensure_command_executed(cmd)
    return stdout_lines


def _first_nonempty_output(cmds: List[str]) -> str:
    for cmd in cmds:
        s_list = _exec(cmd)
        if s_list:
            return "\n".join(s_list)
    return ""


def _parse_profiles_hybrid(std: str) -> List[str]:
    logging.debug(f"프로필 파싱 입력 (첫 200자): {std[:200]}...")
    names = []
    for line in std.splitlines():
        stripped_line = line.strip()
        logging.debug(f"처리 중인 라인: '{stripped_line}'")
        logging.debug(f"처리 중인 라인 (repr): {repr(stripped_line)}")

        profile_name = None
        if "All User Profile     :" in stripped_line:
            profile_name = stripped_line.split("All User Profile     :", 1)[1].strip()
        elif "모든 사용자 프로필     :" in stripped_line:
            profile_name = stripped_line.split("모든 사용자 프로필     :", 1)[1].strip()

        if profile_name:
            logging.debug(f"파싱된 프로필 이름: '{profile_name}'")
            if profile_name and profile_name != "<None>":
                if ',' in profile_name:
                    profile_name = profile_name.split(',')[0].strip()
                if profile_name and not profile_name.isspace():
                    names.append(profile_name)
    logging.debug(f"라인별 파싱으로 발견된 프로필: {names}")
    return names


def _get_profiles_stdout() -> str:
    std = _first_nonempty_output([
        "netsh wlan show profiles",
        "chcp 65001>NUL & netsh wlan show profiles",
    ])
    if not std.strip():
        std = _first_nonempty_output([
            "netsh wlan show profile",
            "chcp 65001>NUL & netsh wlan show profile",
        ])
    return std or ""


def get_wifi_profile_names() -> List[str]:
    """
    시스템에 저장된 Wi-Fi 프로필 목록을 가져옵니다.
    Returns:
        List[str]: Wi-Fi 프로필 이름 리스트.
    """
    std = _get_profiles_stdout()
    if not std.strip():
        logging.warning("Wi-Fi 프로필을 가져올 수 없습니다. netsh wlan show profiles 명령의 출력이 비어 있습니다.")
        return []

    profiles = _parse_profiles_hybrid(std)
    if not profiles:
        logging.warning("Wi-Fi 프로필을 파싱할 수 없습니다. netsh wlan show profiles 명령의 출력 형식을 확인하세요.")
        return []

    return profiles

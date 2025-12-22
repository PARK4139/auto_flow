import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_remote_path_by_user_name(template_path: str, user_name: str) -> Path:
    """
    원격 경로 템플릿과 사용자 이름을 받아 Path 객체를 반환합니다.
    Args:
        template_path (str): 원격 경로 템플릿 (예: "/home/{user_name}/pk_system")
        user_name (str): 원격 서버의 사용자 이름
    Returns:
        Path: 완성된 원격 경로의 Path 객체
    """
    try:
        return Path(template_path.format(user_name=user_name))
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass

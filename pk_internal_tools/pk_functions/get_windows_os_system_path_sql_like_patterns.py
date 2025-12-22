from typing import List, Any

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_windows_os_system_path_sql_like_patterns() -> list[str | Any] | None:
    """
    시스템 관련 경로를 필터링하기 위한 SQL LIKE 패턴 목록을 반환합니다.

    Returns:
        List[str]: 시스템 경로 필터링 패턴 목록입니다.
    """
    try:

        return ["%.git%", "%__pycache__%", "%node_modules%", "%.venv%", "%pk_system%", "%System Volume Information%", "%RECYCLE.BIN%", "%$RECYCLE.BIN%", "%Windows%", "%Program Files%", "%Program Files (x86)%"]
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass

from functools import lru_cache

from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

# pk_* -> ensure_pk_ttl_cached
@ensure_seconds_measured
@ensure_pk_ttl_cached(ttl_seconds=10 * 1 * 1, maxsize=10)
def get_pk_version(project_info=None):
    from pathlib import Path
    import importlib.metadata as im
    try:
        v = im.version('pk_system')  # 'pk-system'도 동일 동작
    except im.PackageNotFoundError:
        # 설치 안 되어 있으면 pyproject 파싱으로 폴백
        from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
        project_info = project_info or get_project_info_from_pyproject()
        v = project_info.get("version", "unknown")

    # 메타데이터에 로컬 버전(+gHASH…)이 없으면, 가능한 경우 git 해시 추가
    if '+' not in v:
        try:
            import subprocess, os
            here = Path(__file__).resolve().parent
            h = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                        cwd=here, text=True).strip()
            if h:
                v = f"{v}+g{h}"
        except Exception as e:
            pass  # 깃 리포가 아니면 그냥 메타데이터 버전 반환
    return v

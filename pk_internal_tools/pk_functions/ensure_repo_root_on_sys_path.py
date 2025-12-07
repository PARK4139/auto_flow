from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

@ensure_seconds_measured
def ensure_repo_root_on_sys_path(__file__) -> None:
    # repo root를 sys.path에 추가하는 이유
    # 기본적으로 Python은 repo root(=프로젝트 최상위 디렉토리) 를 모르는 상태입니다.
    # 그래서 실행할 때마다:
    # PYTHONPATH=/path/to/repo python script.py
    # 이렇게 환경변수를 잡아줘야 하는데, 매번 귀찮습니다.
    # 대신 코드 초반에 repo root를 sys.path에 한 번 넣어두면 → 환경에 상관없이 import가 보장됩니다.

    # repo root를 sys.path에 주입한 뒤, 절대 import로 가져오면 어디서 실행해도 안정적으로 동작합니다.
    """
    Insert the repository root (which has 'pk_internal_tools' as a child)
    to the front of sys.path so that 'pk_tests' can be imported
    regardless of the current working directory.
    """
    from pathlib import Path
    import sys

    here = Path(__file__).resolve()
    # Heuristic: find a parent that contains 'pk_internal_tools' directory
    candidates = [p for p in here.parents if (p / "pk_internal_tools").is_dir()]
    if not candidates:
        return
    repo_root = candidates[0]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)



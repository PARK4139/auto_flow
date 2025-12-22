from pathlib import Path
from typing import List
from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


# @ensure_pk_ttl_cached(ttl_seconds=60 * 60 * 60, maxsize=64)
def get_external_project_root_candidates(start_path: Path = None) -> List[Path]:
    """
    외부 프로젝트의 루트 디렉토리 후보를 찾습니다.
    - pyproject.toml 파일을 기준으로 프로젝트 루트를 식별합니다.
    - 특정 디렉토리는 검색에서 제외합니다.

    Args:
        start_path (Path, optional): 검색을 시작할 경로. 지정하지 않으면 사용자 홈 디렉토리에서 시작합니다.

    Returns:
        List[Path]: 외부 프로젝트의 루트 디렉토리 후보 목록.
    """
    import logging
    import traceback
    from pathlib import Path
    from typing import List

    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

    logging.info(PK_UNDERLINE)
    logging.info(f"외부 프로젝트 루트 후보 찾기 시작")
    logging.info(PK_UNDERLINE)

    if start_path is None:
        start_path = Path.home()

    candidates: List[Path] = []

    # 검색 제외 패턴 (gitignore 패턴과 유사)
    ignore_patterns = [
        ".git", ".venv", "node_modules", "__pycache__", ".vscode",
        ".idea", "build", "dist", ".mypy_cache", ".pytest_cache",
        "*.egg-info", "htmlcov", "venv", ".DS_Store", "target", "env",
        ".svn", ".hg", "tmp", "temp", "pk_logs", ".pk_system", "pk_external_tools_lager_than_4MB",
        "cache", "휴지통" # Added "cache" and "휴지통"
    ]

    logging.info(f"검색 시작 경로: {start_path}")
    logging.info(f"제외 패턴: {', '.join(ignore_patterns)}")

    for pyp_file in start_path.rglob("pyproject.toml"):
        try:
            project_root = pyp_file.parent
            is_ignored = False
            
            # Check if any component of the project_root or its parents (up to start_path)
            # matches any of the ignore_patterns
            current_path_component = project_root
            while current_path_component != start_path.parent and current_path_component != current_path_component.parent: # Iterate up to start_path's parent or root
                for part in current_path_component.parts:
                    if part in ignore_patterns:
                        is_ignored = True
                        break
                if is_ignored:
                    break
                current_path_component = current_path_component.parent

            if is_ignored:
                logging.debug(f"pyproject.toml 파일이 제외 패턴 디렉토리 내에 있습니다: {pyp_file}")
                continue

            if project_root not in candidates:
                candidates.append(project_root)
                logging.info(f"후보 발견: {project_root}")
        except PermissionError:
            logging.warning(f"권한 오류로 인해 {pyp_file} 경로에 접근할 수 없습니다.")
        except Exception as e:
            logging.error(f"pyproject.toml 파일 처리 중 예상치 못한 오류 발생 ({pyp_file}): {e}")
            logging.debug(traceback.format_exc())

    logging.info(f"총 {len(candidates)}개의 외부 프로젝트 루트 후보 발견.")
    logging.info(f"외부 프로젝트 루트 후보 찾기 완료")
    logging.info(PK_UNDERLINE)

    return candidates

"""
프로젝트 내 주요 디렉토리들의 절대 경로를 정의합니다.

이 모듈은 프로젝트의 루트 디렉토리를 자동으로 찾아 시스템 경로에 추가하며,
다양한 환경에서 일관된 경로 참조를 제공합니다.
Pathlib를 사용하여 크로스 플랫폼 호환성을 보장합니다.

중요: 이 모듈은 프로젝트의 다른 모듈에 대한 의존성이 없어야 합니다.
"""
import sys
from pathlib import Path


def _find_project_root_and_add_to_path(start_path: str) -> Path:
    """
    Finds the project root from a start path and adds it to sys.path.
    The project root is identified by the presence of 'pyproject.toml' or '.git'.
    """
    current_path = Path(start_path).resolve()
    if current_path.is_file():
        current_path = current_path.parent

    for parent in [current_path] + list(current_path.parents):
        if (parent / 'pyproject.toml').exists() or (parent / '.git').exists():
            project_root = parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            return project_root
    raise FileNotFoundError(f"Project root not found starting from {start_path}")


# --- Core Path Definitions ---
# This is the single source of truth for the project root.
# Importing this module will have the side-effect of setting up sys.path.
D_PROJECT_ROOT_PATH = _find_project_root_and_add_to_path(__file__)

# --- User-Specific and System Paths ---
D_HOME_PATH = Path.home()
D_DOWNLOADS_PATH = D_HOME_PATH / 'Downloads'
D_DESKTOP_PATH = D_HOME_PATH / 'Desktop'

# This path seems user-specific, constructing it based on Desktop path.
# TODO: This should be configured externally if it differs between users.
D_AUTO_FLOW_REPO = D_PROJECT_ROOT_PATH

# --- Project-Internal Paths (relative to D_PROJECT_ROOT_PATH) ---
D_AUTO_FLOW_INTERNAL_TOOLS_PATH = D_PROJECT_ROOT_PATH / "auto_flow_internal_tools"
D_FUNCTIONS_PATH = D_AUTO_FLOW_INTERNAL_TOOLS_PATH / "functions"
D_WRAPPERS_PATH = D_AUTO_FLOW_INTERNAL_TOOLS_PATH / "wrappers"
D_MVP_WRAPPERS_PATH = D_WRAPPERS_PATH / "mvp"
D_DEMO_WRAPPERS_PATH = D_WRAPPERS_PATH / "demo"

D_DESKTOP = D_DESKTOP_PATH

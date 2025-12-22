"""
pk_system 루트경로 선택 함수 (중복 경로 감지 및 사용자 선택)

외부 프로젝트에서 사용 시 여러 pk_system 루트경로가 감지되면
사용자가 선택할 수 있도록 ensure_value_completed를 사용합니다.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, List

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name


def find_all_pk_paths(search_dir: Optional[Path] = None, max_depth: int = 10) -> List[Path]:
    """
    모든 pk_system 루트경로를 찾는 함수
    
    Args:
        search_dir: 검색 시작 디렉토리 (None이면 현재 작업 디렉토리)
        max_depth: 최대 검색 깊이
    
    Returns:
        List[Path]: 발견된 모든 pk_system 루트경로 리스트
    """
    if search_dir is None:
        search_dir = Path.cwd().resolve()
    else:
        search_dir = Path(search_dir).resolve()

    found_paths = []
    visited = set()

    current = search_dir
    depth = 0

    while depth < max_depth:
        # pk_internal_tools 디렉토리가 있는지 확인
        pk_candidate = current / 'pk_internal_tools'
        if pk_candidate.exists() and pk_candidate.is_dir():
            # pyproject.toml 확인
            pyproject_toml = current / 'pyproject.toml'
            if pyproject_toml.exists():
                try:
                    import toml
                    config = toml.load(pyproject_toml)
                    if config.get('project', {}).get('name') == 'pk_system':
                        if str(current) not in visited:
                            found_paths.append(current)
                            visited.add(str(current))
                except Exception as e:
                    pass
            else:
                # pyproject.toml이 없어도 pk_internal_tools가 있으면 추가
                if str(current) not in visited:
                    found_paths.append(current)
                    visited.add(str(current))

        # 상위 디렉토리로 이동
        parent = current.parent
        if parent == current:  # 루트 디렉토리에 도달
            break
        current = parent
        depth += 1

    # __file__ 기반 경로도 확인
    try:
        file_based_path = Path(__file__).resolve().parent.parent.parent
        if (file_based_path / 'pk_internal_tools').exists():
            if str(file_based_path) not in visited:
                found_paths.append(file_based_path)
                visited.add(str(file_based_path))
    except Exception as e:
        pass

    return found_paths


def is_cloned_path(path: Path) -> bool:
    """경로가 외부 프로젝트 내 클론된 assets/pk_system인지 확인"""
    try:
        parent = path.parent
        return parent.name == 'assets' and path.name == 'pk_system'
    except Exception as e:
        return False


def ensure_pk_root_selected(
        search_dir: Optional[Path] = None,
        interactive: bool = True,
        prefer_cloned: bool = True
) -> Optional[Path]:
    """
    pk_system 루트경로를 선택하는 함수 (중복 경로 감지 시 사용자 선택)
    
    Args:
        search_dir: 검색 시작 디렉토리 (None이면 현재 작업 디렉토리)
        interactive: 사용자 선택 활성화 여부 (False면 자동 선택)
        prefer_cloned: 클론된 경로 우선 선택 여부
    
    Returns:
        Path: 선택된 pk_system 루트경로 (None이면 선택 실패)
    """
    # 1. 환경변수 확인 (최우선)
    pk_root_env = os.environ.get('D_PK_ROOT')
    if pk_root_env:
        root = Path(pk_root_env).resolve()
        if root.exists() and (root / 'pk_internal_tools').exists():
            return root

    # 2. 모든 pk_system 루트경로 찾기
    all_paths = find_all_pk_paths(search_dir)

    if not all_paths:
        # 경로를 찾지 못한 경우
        logging.warning("⚠️ pk_system 루트경로를 찾을 수 없습니다.")
        return None

    if len(all_paths) == 1:
        # 경로가 하나만 있는 경우
        return all_paths[0]

    # 3. 여러 경로가 있는 경우
    # logging.warning(f"⚠️ 중복 pk_system 루트경로 발견 ({len(all_paths)}개)")

    # 클론된 경로와 원본 경로 분리
    cloned_paths = [p for p in all_paths if is_cloned_path(p)]
    original_paths = [p for p in all_paths if not is_cloned_path(p)]

    # 4. 자동 선택 (interactive=False인 경우)
    if not interactive:
        if prefer_cloned and cloned_paths:
            selected = cloned_paths[0]
            logging.info(f"자동 선택 (클론된 경로 우선): {selected}")
            return selected
        elif original_paths:
            selected = original_paths[0]
            logging.info(f"자동 선택 (원본 경로): {selected}")
            return selected
        else:
            selected = all_paths[0]
            logging.info(f"자동 선택 (첫 번째 경로): {selected}")
            return selected

    # 5. 사용자 선택 (interactive=True인 경우)
    try:
        # 경로 옵션 준비
        path_options = []
        path_descriptions = []

        # 클론된 경로 우선 표시
        for path in cloned_paths:
            path_str = str(path)
            path_options.append(path_str)
            path_descriptions.append(f"[클론됨] {path_str}")

        for path in original_paths:
            path_str = str(path)
            if path_str not in path_options:
                path_options.append(path_str)
                path_descriptions.append(f"[원본] {path_str}")

        # 사용자에게 선택 요청
        logging.info("")
        logging.info("=" * 60)
        logging.info("🔍 중복 pk_system 루트경로 감지")
        logging.info("=" * 60)
        logging.info("")
        logging.info("다음 경로 중 하나를 선택하세요:")
        logging.info("")

        for idx, (path_str, desc) in enumerate(zip(path_options, path_descriptions), 1):
            logging.info(f" {idx}. {desc}")

        logging.info("")

        # ensure_value_completed 사용 (fzf 또는 입력)
        pk_path_selection = ensure_env_var_completed(
            key_name="pk_path_selection",
            func_n=get_caller_name(),
            options=path_options,
            guide_text="pk_system 루트경로를 선택하세요:",
        )

        if pk_path_selection:
            selected_path = Path(pk_path_selection).resolve()
            if selected_path.exists() and (selected_path / 'pk_internal_tools').exists():
                logging.info(f"선택된 경로: {selected_path}")

                # 선택된 경로를 환경변수로 설정 (다음 호출 시 우선 사용)
                os.environ['D_PK_ROOT'] = str(selected_path)

                return selected_path
            else:
                logging.error(f"선택된 경로가 유효하지 않습니다: {selected_path}")
                return None
        else:
            logging.warning("⚠️ 경로 선택이 취소되었습니다.")
            # 기본값 반환 (클론된 경로 우선)
            if prefer_cloned and cloned_paths:
                return cloned_paths[0]
            elif original_paths:
                return original_paths[0]
            return all_paths[0]

    except Exception as e:
        logging.error(f"경로 선택 중 오류 발생: {e}")
        # 오류 발생 시 기본값 반환
        if prefer_cloned and cloned_paths:
            return cloned_paths[0]
        elif original_paths:
            return original_paths[0]
        return all_paths[0] if all_paths else None


def ensure_pk_path_resolved(
        remove_from_sys_path: bool = True,
        interactive: bool = True
) -> Optional[Path]:
    """
    pk_system 루트경로를 해결하고 sys.path 충돌 제거
    
    Args:
        remove_from_sys_path: sys.path에서 다른 pk_system 루트경로 제거 여부
        interactive: 중복 경로 감지 시 사용자 선택 활성화 여부
    
    Returns:
        Path: 선택된 pk_system 루트경로
    """
    # 1. pk_system 루트경로 선택
    selected_path = ensure_pk_root_selected(interactive=interactive)

    if selected_path is None:
        return None

    # 2. sys.path에서 다른 pk_system 루트경로 제거
    if remove_from_sys_path:
        selected_path_str = str(selected_path)
        removed_paths = []

        # sys.path에서 다른 pk_system 루트경로 제거
        new_sys_path = []
        for path_str in sys.path:
            path_obj = Path(path_str) if path_str else None
            if path_obj:
                # pk_system 루트경로인지 확인
                pk_internal_tools = path_obj / 'pk_internal_tools'
                if pk_internal_tools.exists() or 'pk_internal_tools' in str(path_obj):
                    # 선택된 경로가 아니면 제거
                    if str(path_obj.resolve()) != selected_path_str:
                        removed_paths.append(str(path_obj))
                        continue
            new_sys_path.append(path_str)

        if removed_paths:
            logging.info("🔧 sys.path에서 충돌하는 pk_system 루트경로 제거:")
            for removed in removed_paths:
                logging.info(f"sys.path에서 제거됨?: {removed}")
        sys.path = new_sys_path

        # 선택된 경로가 sys.path에 없으면 추가
        if selected_path_str not in sys.path:
            sys.path.insert(0, selected_path_str)
            logging.info(f"sys.path에 추가: {selected_path_str}")

    return selected_path

import logging
import os
import traceback
from pathlib import Path
from typing import List, Optional

# Lazy import for core pk_system functions
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from dotenv import load_dotenv, set_key, dotenv_values

# Initialize logging for this module
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

# Load .env file at module level
load_dotenv()

def _get_key_for_env_var(key_name: str, func_n: str) -> str:
    """
    key_name과 func_n을 기반으로 환경 변수 키를 생성합니다.
    ensure_env_var_complete() 내부의 ID 생성 방식과 유사합니다.
    """
    # 불필요한 공백 제거 및 대문자 변환, 특수 문자 제거 (환경 변수 명명 규칙 준수)
    cleaned_key_name = "".join(filter(str.isalnum, key_name.upper()))
    cleaned_func_n = "".join(filter(str.isalnum, func_n.upper()))
    
    # 예: PK_PATH_INSTALL_PK_SYSTEM_GET_INSTALL_PATH
    return f"{cleaned_key_name}_{cleaned_func_n}"


def ensure_env_var_path_candidate_completed(
    key_name: str,
    func_n: str,
    guide_text: str,
    search_pattern: str = "**/*",  # 찾을 파일/디렉토리 패턴 (예: "*.py", "my_project")
    search_start_path: Optional[Path] = None,
    depth_limit: int = 5,
    ignore_dirs: Optional[List[str]] = None
) -> Optional[str]:
    """
    .env 파일에서 환경 변수 경로를 가져오거나, 없다면 사용자에게 입력받아 저장합니다.

    Args:
        key_name (str): 환경 변수를 식별할 이름 (예: "PK_INSTALL_PATH").
        func_n (str): 호출 함수 이름 (예: "get_install_path").
        guide_text (str): 사용자에게 경로를 선택하도록 안내할 텍스트.
        search_pattern (str): 상위 경로를 탐색하며 찾을 파일/디렉토리의 glob 패턴.
        search_start_path (Optional[Path]): 경로 탐색을 시작할 경로. None이면 현재 작업 디렉토리.
        depth_limit (int): 상위 경로 탐색 깊이 제한.
        ignore_dirs (Optional[List[str]]): 경로 탐색 시 무시할 디렉토리 이름 리스트.

    Returns:
        Optional[str]: .env에 저장된 (또는 새로 저장된) 경로 값. 없으면 None.
    """
    env_var_key = _get_key_for_env_var(key_name, func_n)
    dotenv_path = Path(".env") # Assuming .env is in the project root or current dir

    # 1. .env에 값이 있는지 확인
    env_values = dotenv_values(dotenv_path=dotenv_path)
    if env_var_key in env_values and env_values[env_var_key]:
        logger.info(f".env에서 기존 경로 값 발견: {env_var_key}={env_values[env_var_key]}")
        return env_values[env_var_key]

    logger.info(f".env에 {env_var_key} 경로 값이 없습니다. 탐색을 시작합니다.")

    # 2. .env에 값이 없다면, 상위 경로를 돌면서 후보 경로 수집
    candidates: List[Path] = []
    current_path = search_start_path if search_start_path else Path.cwd()
    
    for _ in range(depth_limit):
        logger.debug(f"현재 탐색 경로: {current_path}, 패턴: {search_pattern}")
        # 현재 경로에서 패턴에 맞는 파일/디렉토리 검색
        # glob 패턴에 따라 동작이 달라질 수 있으므로 더 정교한 로직 필요
        found_items = list(current_path.glob(search_pattern))
        for item in found_items:
            if ignore_dirs and item.is_dir() and item.name in ignore_dirs:
                logger.debug(f"무시할 디렉토리: {item}")
                continue
            candidates.append(item.resolve()) # 절대 경로로 저장

        if current_path == current_path.parent: # 루트 디렉토리에 도달하면 중지
            break
        current_path = current_path.parent
        
        # 깊이 제한을 둠으로써 너무 많이 상위로 올라가지 않도록
        if _ >= depth_limit -1 and not candidates:
            logger.warning(f"탐색 깊이 {depth_limit} 이내에서 {search_pattern} 패턴에 맞는 후보 경로를 찾지 못했습니다.")

    unique_candidates = sorted(list(set(candidates))) # 중복 제거 및 정렬
    candidate_strings = [str(p) for p in unique_candidates] # type: ignore

    selected_path: Optional[str] = None

    if not candidate_strings:
        logger.warning(f"{search_pattern} 패턴에 맞는 후보 경로를 찾지 못했습니다. 사용자에게 직접 입력 요청.")
        selected_path = ensure_value_completed(
            key_name=f"{env_var_key}_DIRECT_INPUT",
            func_n=func_n,
            guide_text=f"{guide_text} (후보가 없습니다. 직접 입력하세요):",
            options=[],
        )
    elif len(candidate_strings) == 1:
        logger.info(f"단일 후보 경로 발견: {candidate_strings[0]}. 자동으로 선택합니다.")
        selected_path = candidate_strings[0]
    else: # 후보 경로가 2개 이상이면 사용자에게 선택 요청
        logger.info(f"후보 경로 {len(candidate_strings)}개 발견. 사용자에게 선택을 요청합니다.")
        selected_path = ensure_value_completed(
            key_name=env_var_key,
            func_n=func_n,
            guide_text=guide_text,
            options=candidate_strings,
        )

    # 3. 입력받은 것을 .env에 저장
    if selected_path:
        try:
            # .env 파일이 없으면 생성
            if not dotenv_path.exists():
                dotenv_path.touch()
                logger.info(f".env 파일이 없어 생성했습니다: {dotenv_path}")
            
            set_key(str(dotenv_path), env_var_key, selected_path)
            # load_dotenv(override=True) # 변경사항 즉시 반영
            logger.info(f"선택된 경로를 .env에 저장했습니다: {env_var_key}={selected_path}")
            # .env 파일 변경 후 환경 변수를 다시 로드하여 현재 프로세스에 적용
            load_dotenv(override=True)
            return selected_path
        except Exception as e:
            logger.error(f".env 파일에 경로 저장 중 오류 발생: {e}", exc_info=True)
            ensure_debugged_verbose(traceback=traceback.format_exc())
            return None
    else:
        logger.warning("경로가 선택되지 않았습니다. .env에 저장하지 않습니다.")
        return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # Test 1: .env에 값이 없는 경우 (후보가 2개 이상)
    # 임시 .env 파일 생성 및 키 삭제
    temp_dotenv_path = Path(".env.test")
    if temp_dotenv_path.exists():
        os.remove(temp_dotenv_path)
    
    # 임시 테스트 디렉토리 구조 생성
    temp_dir = Path("./temp_test_dir")
    temp_dir.mkdir(exist_ok=True)
    (temp_dir / "subdir1").mkdir(exist_ok=True)
    (temp_dir / "subdir2").mkdir(exist_ok=True)
    (temp_dir / "subdir1" / "target_file_A.txt").touch()
    (temp_dir / "subdir2" / "target_file_B.txt").touch()
    (temp_dir.parent / "another_target_file.txt").touch()


    logger.info("\n--- Test 1: .env에 값이 없고, 후보가 여러 개인 경우 ---")
    func_name = get_caller_name()
    selected = ensure_env_var_path_candidate_completed(
        key_name="TEST_PATH_MULTI",
        func_n=func_name,
        guide_text="테스트할 경로를 선택하세요 (여러 후보)",
        search_pattern="**/*.txt",
        search_start_path=temp_dir.parent,
        depth_limit=2,
        ignore_dirs=["temp_test_dir"]
    )
    logger.info(f"Test 1 결과: {selected}")
    if selected:
        assert selected == os.getenv("TEST_PATH_MULTI_ENSUREENVVARPATHCOMPLETED")

    # Test 2: .env에 값이 없는 경우 (단일 후보)
    logger.info("\n--- Test 2: .env에 값이 없고, 후보가 하나인 경우 ---")
    (temp_dir / "single_candidate.json").touch()
    (temp_dir / "subdir1" / "target_file_A.txt").unlink() # 다른 후보 제거
    (temp_dir / "subdir2" / "target_file_B.txt").unlink()
    (temp_dir.parent / "another_target_file.txt").unlink()


    selected = ensure_env_var_path_candidate_completed(
        key_name="TEST_PATH_SINGLE",
        func_n=func_name,
        guide_text="테스트할 경로를 선택하세요 (단일 후보)",
        search_pattern="**/*.json",
        search_start_path=temp_dir.parent,
        depth_limit=2
    )
    logger.info(f"Test 2 결과: {selected}")
    if selected:
        assert selected == os.getenv("TEST_PATH_SINGLE_ENSUREENVVARPATHCOMPLETED")

    # Test 3: .env에 값이 있는 경우
    logger.info("\n--- Test 3: .env에 값이 이미 있는 경우 ---")
    os.environ["TEST_PATH_EXISTING_ENSUREENVVARPATHCOMPLETED"] = "/path/from/env"
    selected = ensure_env_var_path_candidate_completed(
        key_name="TEST_PATH_EXISTING",
        func_n=func_name,
        guide_text="테스트할 경로를 선택하세요 (이미 .env에 있음)",
        search_pattern="**/*",
        search_start_path=temp_dir.parent
    )
    logger.info(f"Test 3 결과: {selected}")
    assert selected == "/path/from/env"
    
    # Test 4: 후보가 없는 경우
    logger.info("\n--- Test 4: 후보가 없는 경우 ---")
    os.remove(temp_dir / "single_candidate.json")
    
    selected = ensure_env_var_path_candidate_completed(
        key_name="TEST_PATH_NO_CANDIDATE",
        func_n=func_name,
        guide_text="테스트할 경로를 선택하세요 (후보 없음)",
        search_pattern="**/*.xyz",
        search_start_path=temp_dir.parent
    )
    logger.info(f"Test 4 결과: {selected}")
    assert selected is None # 사용자가 아무것도 선택하지 않으면 None 반환 가정
    
    # 임시 파일 및 디렉토리 정리
    if temp_dotenv_path.exists():
        os.remove(temp_dotenv_path)
    import shutil
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    logger.info("\n--- 모든 테스트 완료 ---")

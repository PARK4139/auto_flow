from pathlib import Path
from typing import List, Dict, Optional, Tuple
import os
import subprocess
import logging
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def ensure_target_file_contents_found(
    search_string: str,
    search_paths: Optional[List[str]] = None,
    pk_file_extensions: Optional[List[str]] = None,
    exclude_paths: Optional[List[str]] = None,
    case_sensitive: bool = False,
    max_file_size_mb: int = 10,
    use_grep: bool = True
) -> List[Dict[str, str]]:
    """
    파일 내용에서 특정 문자열을 검색하는 함수
    
    Args:
        search_string: 검색할 문자열
        search_paths: 검색할 경로 리스트 (None이면 현재 디렉토리)
        pk_file_extensions: 검색할 파일 확장자 리스트 (None이면 모든 파일)
        exclude_paths: 제외할 경로 리스트
        case_sensitive: 대소문자 구분 여부
        max_file_size_mb: 검색할 최대 파일 크기 (MB)
        use_grep: grep 명령어 사용 여부 (False면 Python 내장 검색)
    
    Returns:
        검색 결과 리스트 (파일 경로, 라인 번호, 라인 내용 포함)
    """
    
    if not search_string.strip():
        logging.debug("검색 문자열이 비어있습니다.")
        return []
    
    # 기본 검색 경로 설정
    if search_paths is None:
        search_paths = [str(Path.cwd())]
    
    # 기본 제외 경로 설정
    if exclude_paths is None:
        exclude_paths = [
            ".git", ".venv", "__pycache__", "node_modules",
            ".pytest_cache", ".mypy_cache", ".coverage"
        ]
    
    # 기본 파일 확장자 설정
    if pk_file_extensions is None:
        pk_file_extensions = [".txt", ".py", ".md", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".log"]
    
    logging.debug(f"파일 내용에서 '{search_string}' 검색을 시작합니다...")
    logging.debug(f"검색 경로: {', '.join(search_paths)}")
    logging.debug(f"파일 확장자: {', '.join(pk_file_extensions)}")
    
    if use_grep and _is_grep_available():
        return _search_with_grep(search_string, search_paths, pk_file_extensions, exclude_paths, case_sensitive, max_file_size_mb)
    else:
        return _search_with_python(search_string, search_paths, pk_file_extensions, exclude_paths, case_sensitive, max_file_size_mb)


def _is_grep_available() -> bool:
    """grep 명령어 사용 가능 여부 확인"""
    try:
        result = subprocess.run(["grep", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


@ensure_seconds_measured
def _search_with_grep(
    search_string: str,
    search_paths: List[str],
    pk_file_extensions: List[str],
    exclude_paths: List[str],
    case_sensitive: bool,
    max_file_size_mb: int
) -> List[Dict[str, str]]:
    """grep을 사용한 파일 내용 검색"""
    
    results = []
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            logging.debug(f"경로가 존재하지 않습니다: {search_path}")
            continue
        
        # grep 명령어 구성
        cmd = ["grep", "-r", "-n"]
        
        if not case_sensitive:
            cmd.append("-i")
        
        # 파일 확장자 필터링
        for ext in pk_file_extensions:
            cmd.extend(["--include", f"*{ext}"])
        
        # 제외 경로 설정
        for exclude_path in exclude_paths:
            cmd.extend(["--exclude-dir", exclude_path])
        
        # 검색 문자열과 경로 추가
        cmd.extend([search_string, search_path])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parsed_result = _parse_grep_output(line)
                        if parsed_result:
                            results.append(parsed_result)
            
        except subprocess.TimeoutExpired:
            logging.debug(f"검색 시간 초과: {search_path}")
        except subprocess.SubprocessError as e:
            logging.debug(f"grep 실행 오류: {e}")
    
    return results


def _parse_grep_output(grep_line: str) -> Optional[Dict[str, str]]:
    """grep 출력 결과를 파싱"""
    try:
        # grep 출력 형식: file_path:line_number:content
        parts = grep_line.split(':', 2)
        if len(parts) >= 3:
            return {
                "file_path": parts[0],
                "line_number": parts[1],
                "line_content": parts[2],
                "search_method": "grep"
            }
    except Exception:
        pass
    return None


@ensure_seconds_measured
def _search_with_python(
    search_string: str,
    search_paths: List[str],
    pk_file_extensions: List[str],
    exclude_paths: List[str],
    case_sensitive: bool,
    max_file_size_mb: int
) -> List[Dict[str, str]]:
    """Python 내장 기능을 사용한 파일 내용 검색"""
    
    results = []
    max_file_size_bytes = max_file_size_mb * 1024 * 1024
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
        
        for root, dirs, files in os.walk(search_path):
            # 제외 디렉토리 필터링
            dirs[:] = [d for d in dirs if d not in exclude_paths]
            
            for file in files:
                # 파일 확장자 확인
                if not any(file.endswith(ext) for ext in pk_file_extensions):
                    continue
                
                file_path = os.path.join(root, file)
                
                try:
                    # 파일 크기 확인
                    if os.path.getsize(file_path) > max_file_size_bytes:
                        continue
                    
                    # 파일 내용 검색
                    file_results = _search_in_file(file_path, search_string, case_sensitive)
                    results.extend(file_results)
                    
                except (OSError, UnicodeDecodeError) as e:
                    # 파일 읽기 오류는 무시하고 계속 진행
                    continue
    
    return results


def _search_in_file(file_path: str, search_string: str, case_sensitive: bool) -> List[Dict[str, str]]:
    """개별 파일에서 문자열 검색"""
    
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if case_sensitive:
                    if search_string in line:
                        results.append({
                            "file_path": file_path,
                            "line_number": str(line_num),
                            "line_content": line.rstrip('\n'),
                            "search_method": "python"
                        })
                else:
                    if search_string.lower() in line.lower():
                        results.append({
                            "file_path": file_path,
                            "line_number": str(line_num),
                            "line_content": line.rstrip('\n'),
                            "search_method": "python"
                        })
    except Exception:
        pass
    
    return results


def print_search_results(results: List[Dict[str, str]], max_results: int = 50) -> None:
    """검색 결과를 출력"""
    
    if not results:
        logging.debug("검색 결과가 없습니다.")
        return
    
    logging.debug(f"총 {len(results)}개의 검색 결과를 찾았습니다.")
    
    if len(results) > max_results:
        logging.debug(f"처음 {max_results}개 결과만 표시합니다. (전체: {len(results)}개)")
        results = results[:max_results]
    
    for i, result in enumerate(results, 1):
        logging.debug(f"--- 결과 {i} ---")
        logging.debug(f"파일: {result['file_path']}")
        logging.debug(f"라인: {result['line_number']}")
        logging.debug(f"내용: {result['line_content']}")
        logging.debug(f"검색 방법: {result['search_method']}")


def save_search_results_to_file(results: List[Dict[str, str]], output_file: str) -> None:
    """검색 결과를 파일에 저장"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"검색 결과 - 총 {len(results)}개\n")
            f.write(PK_UNDERLINE + "\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"--- 결과 {i} ---\n")
                f.write(f"파일: {result['file_path']}\n")
                f.write(f"라인: {result['line_number']}\n")
                f.write(f"내용: {result['line_content']}\n")
                f.write(f"검색 방법: {result['search_method']}\n\n")
        
        logging.debug(f"검색 결과가 {output_file}에 저장되었습니다.")
        
    except Exception as e:
        logging.debug(f"파일 저장 오류: {e}")


# 사용 예시 및 테스트 함수
def test_file_contents_search():
    """파일 내용 검색 테스트"""
    
    # 테스트 검색
    search_string = "def ensure_"
    search_paths = ["pk_external_tools/pk_functions"]
    pk_file_extensions = [".py"]
    
    logging.debug("파일 내용 검색 테스트를 시작합니다...")
    
    results = ensure_target_file_contents_found(
        search_string=search_string,
        search_paths=search_paths,
        pk_file_extensions=pk_file_extensions,
        case_sensitive=False,
        max_file_size_mb=5
    )
    
    # 결과 출력
    print_search_results(results)
    
    # 결과 저장
    if results:
        save_search_results_to_file(results, "search_results.txt")
    
    return results


# 간단한 래퍼 함수들
def find_text_in_files(text: str, path: str = ".", extensions: List[str] = None) -> List[Dict[str, str]]:
    """간단한 텍스트 검색 함수"""
    if extensions is None:
        extensions = [".py", ".txt", ".md", ".json"]
    
    return ensure_target_file_contents_found(
        search_string=text,
        search_paths=[path],
        pk_file_extensions=extensions,
        case_sensitive=False
    )


def find_python_functions(function_name: str, path: str = ".") -> List[Dict[str, str]]:
    """Python 함수 정의 검색"""
    return ensure_target_file_contents_found(
        search_string=f"def {function_name}",
        search_paths=[path],
        pk_file_extensions=[".py"],
        case_sensitive=False
    )


def find_imports(module_name: str, path: str = ".") -> List[Dict[str, str]]:
    """특정 모듈 import 검색"""
    return ensure_target_file_contents_found(
        search_string=f"import {module_name}",
        search_paths=[path],
        pk_file_extensions=[".py"],
        case_sensitive=False
    )


def find_from_imports(module_name: str, path: str = ".") -> List[Dict[str, str]]:
    """from import 구문 검색"""
    return ensure_target_file_contents_found(
        search_string=f"from {module_name}",
        search_paths=[path],
        pk_file_extensions=[".py"],
        case_sensitive=False
    )


def find_comments(comment_text: str, path: str = ".") -> List[Dict[str, str]]:
    """주석 내용 검색"""
    return ensure_target_file_contents_found(
        search_string=comment_text,
        search_paths=[path],
        pk_file_extensions=[".py", ".js", ".ts", ".cpp", ".c", ".java"],
        case_sensitive=False
    )


def find_config_values(key: str, path: str = ".") -> List[Dict[str, str]]:
    """설정 파일에서 특정 키 검색"""
    return ensure_target_file_contents_found(
        search_string=key,
        search_paths=[path],
        pk_file_extensions=[".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"],
        case_sensitive=False
    )


# 대화형 검색 함수
def interactive_file_search():
    """대화형 파일 내용 검색"""
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    
    logging.debug("파일 내용 검색 도구")
    
    # 검색 문자열 입력
    search_string = ensure_value_completed_2025_10_12_0000("검색할 문자열을 입력하세요: ")
    if not search_string:
        logging.debug("검색 문자열이 입력되지 않았습니다.")
        return
    
    # 검색 경로 입력
    func_n = get_caller_name()
    search_path = ensure_value_completed_2025_11_11(
        key_name="search_path",
        func_n=func_n,
        options=["."],  # 기본값으로 현재 디렉토리 포함
        guide_text="검색할 경로를 입력하세요 (기본값: 현재 디렉토리):",
        history_reset=False
    ) or "."  # 선택이 없으면 기본값 사용
    
    # 파일 확장자 선택
    logging.debug("검색할 파일 확장자를 선택하세요:")
    logging.debug("1. Python 파일만 (.py)")
    logging.debug("2. 텍스트 파일 (.txt, .md)")
    logging.debug("3. 설정 파일 (.toml, .yaml, .json)")
    logging.debug("4. 모든 파일")
    
    choice = ensure_value_completed_2025_10_12_0000("선택 (1-4): ", default="1")
    
    if choice == "1":
        extensions = [".py"]
    elif choice == "2":
        extensions = [".txt", ".md"]
    elif choice == "3":
        extensions = [".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"]
    else:
        extensions = None
    
    # 대소문자 구분 여부
    case_sensitive = ensure_value_completed_2025_10_12_0000("대소문자를 구분하시겠습니까? (y/n): ", default="n").lower() == "y"
    
    # 검색 실행
    logging.debug(f"'{search_string}'를 '{search_path}'에서 검색합니다...")
    
    results = ensure_target_file_contents_found(
        search_string=search_string,
        search_paths=[search_path],
        pk_file_extensions=extensions,
        case_sensitive=case_sensitive
    )
    
    # 결과 출력
    print_search_results(results)
    
    # 결과 저장 여부
    if results:
        save_choice = ensure_value_completed_2025_10_12_0000("검색 결과를 파일로 저장하시겠습니까? (y/n): ", default="y").lower() == "y"
        if save_choice:
            output_file = ensure_value_completed_2025_10_12_0000("저장할 파일명을 입력하세요: ", default="search_results.txt")
            save_search_results_to_file(results, output_file)
    
    return results


if __name__ == "__main__":
    # 테스트 실행
    test_file_contents_search()
    
    # 대화형 검색 실행 (선택사항)
    # interactive_file_search()

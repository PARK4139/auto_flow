from pathlib import Path


def ensure_filename_unique_in_d_working(d_working: Path, filename: str) -> None:
    """
    디렉토리(d_working) 하위에서 파일명이 중복되는지 확인하고, 중복이 있으면 에러를 발생시키는 함수
    
    Args:
        d_working: 검색할 디렉토리 경로
        filename: 확인할 파일명 (확장자 포함)
    
    Raises:
        ValueError: 중복 파일명이 발견된 경우
    """
    import os
    
    d_working_path = Path(d_working).resolve()
    
    if not d_working_path.exists() or not d_working_path.is_dir():
        return
    
    found_paths = []
    for root, _, filenames in os.walk(d_working_path):
        if filename in filenames:
            found_path = Path(root) / filename
            found_paths.append(found_path.resolve())
    
    if len(found_paths) > 1:
        error_message = (
            f"중복 파일명 발견: '{filename}'\n"
            f"검색 디렉토리: {d_working_path}\n"
            f"발견된 경로들 ({len(found_paths)}개):\n" +
            "\n".join(f"  - {p}" for p in found_paths)
        )
        raise ValueError(error_message)


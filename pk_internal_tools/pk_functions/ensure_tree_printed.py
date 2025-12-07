import logging
from pathlib import Path

def ensure_tree_printed(
    d_target: Path,
    indent_char: str = '    ',
    max_depth: int = -1,
    mode: str = "all"  # "files", "dirs", "all"
):
    """
    지정된 디렉토리의 트리 구조를 출력합니다.

    Args:
        d_target (Path): 트리 구조를 출력할 대상 디렉토리의 Path 객체.
        indent_char (str): 각 깊이 레벨에 사용할 들여쓰기 문자열 (기본값: 공백 4개).
        max_depth (int): 출력할 최대 깊이. -1은 제한 없음을 의미합니다 (기본값: -1).
        mode (str): 출력 모드 ("files", "dirs", "all")
    """
    # lazy import
    try:
        import os
    except ImportError:
        logging.error("os 모듈을 임포트할 수 없습니다.")
        return

    if not d_target.is_dir():
        logging.warning(f"'{d_target}'은(는) 유효한 디렉토리가 아닙니다.")
        return

    logging.debug(f"{d_target}")

    for root, dirs, files in os.walk(d_target):
        try:
            current_relative_path = Path(root).relative_to(d_target)
            level = len(current_relative_path.parts) if current_relative_path.parts else 0
        except ValueError:
            level = 0

        if max_depth != -1 and level > max_depth:
            continue

        indent = indent_char * level
        sub_indent = indent + indent_char

        # 디렉토리 출력
        if mode in ("dirs", "all"):
            logging.debug(f"{indent}├── {Path(root).name}/")

        # 파일 출력
        if mode in ("files", "all"):
            for f in sorted(files):
                logging.debug(f"{sub_indent}└── {f}")

from pathlib import Path
from typing import Optional


def get_line_number_from_file(*, file_path: Path, text: str, from_reverse_mode: bool = True) -> Optional[int]:
    import logging

    from pk_internal_tools.pk_functions.get_nx import get_nx
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        if from_reverse_mode:
            # 뒤에서부터 검색
            for i in range(len(lines) - 1, -1, -1):
                if text in lines[i]:
                    # 파일 끝에서부터의 줄 번호 (1부터 시작)
                    return len(lines) - i
        else:
            # 앞에서부터 검색
            for i, line in enumerate(lines):
                if text in line:
                    # 파일 시작에서부터의 줄 번호 (1부터 시작)
                    return i + 1

        logging.info(f"파일 '{get_nx(file_path)}'에서 '{text[:10]}...'를 찾을 수 없습니다.")
        return None

    except FileNotFoundError:
        logging.error(f"FILE NOT FOUND {get_nx(file_path)}")
        return None
    except Exception as e:
        logging.error(f"파일 '{get_nx(file_path)}'에서 줄 번호를 가져오는 중 오류 발생: {e}")
        return None

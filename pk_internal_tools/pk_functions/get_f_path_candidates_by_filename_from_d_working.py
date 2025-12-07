from pathlib import Path
from typing import Optional

import logging


def get_f_path_candidates_by_filename_from_d_working(
    d_working: Path, 
    filename: str,
    additional_paths: Optional[list[tuple[Path, str]]] = None
) -> Optional[list[Path]]:
    """
    디렉토리(d_working) 하위를 walking하면서 파일명과 일치하는 파일의 후보 경로들을 찾아서 반환하는 함수
    
    Args:
        d_working: 검색할 디렉토리 경로
        filename: 찾을 파일명 (확장자 포함)
        additional_paths: 추가 경로 옵션 리스트 [(Path, description), ...]
            - Path: 생성할 파일 경로
            - description: 경로 설명 (예: "프로젝트 루트 (생성예정)")
    
    Returns:
        Optional[list[Path]]: 찾은 파일의 경로 목록
            - 파일이 없으면 None
            - 파일이 1개면 [Path] 반환
            - 파일이 여러 개면 사용자 입력을 받아 선택된 경로 [Path] 반환
            - 사용자가 취소하면 None 반환
            - 추가 경로를 선택한 경우 해당 Path 반환 (파일이 없어도 생성 가능)
    """
    import os
    
    d_working_path = Path(d_working).resolve()
    
    if not d_working_path.exists() or not d_working_path.is_dir():
        return None
    
    # 파일 검색 및 중복 체크를 동시에 수행
    found_paths = []
    for root, _, filenames in os.walk(d_working_path):
        if filename in filenames:
            found_path = Path(root) / filename
            found_paths.append(found_path.resolve())
    
    if len(found_paths) == 0:
        return None
    
    # 중복 체크: 여러 개면 사용자에게 선택 요청
    # 추가 경로 옵션이 있으면 함께 표시
    total_options = len(found_paths)
    if additional_paths:
        total_options += len(additional_paths)
    
    if len(found_paths) > 1 or (len(found_paths) > 0 and additional_paths):
        # print를 사용하여 로그 포맷 없이 직접 출력
        print("")
        print("_" * 66)
        print("# 중복 파일명 발견")
        print(f"파일명: '{filename}'")
        print(f"검색 디렉토리: {d_working_path}")
        print(f"발견된 경로: {len(found_paths)}개")
        print("")
        print("_" * 66)
        print("# 사용할 경로를 선택하세요")
        
        # 기존 발견된 경로 표시
        for idx, path in enumerate(found_paths, start=1):
            print(f"{idx}. {path}")
        
        # 추가 경로 옵션 표시
        if additional_paths:
            start_idx = len(found_paths) + 1
            for idx, (path, description) in enumerate(additional_paths, start=start_idx):
                print(f"{idx}. {path} ({description})")
        
        print("")
        
        # 사용자 입력으로 경로 선택
        while True:
            try:
                cancel_hint = "또는 'q'로 취소"
                selection = input(f"선택 (1-{total_options}) {cancel_hint}: ").strip()
                
                if selection.lower() == 'q':
                    print("사용자가 취소했습니다.")
                    return None
                
                selected_idx = int(selection)
                
                # 기존 발견된 경로 선택
                if 1 <= selected_idx <= len(found_paths):
                    selected_path = found_paths[selected_idx - 1]
                    print(f"선택된 경로: {selected_path}")
                    return [selected_path]
                
                # 추가 경로 옵션 선택
                elif additional_paths and len(found_paths) < selected_idx <= total_options:
                    additional_idx = selected_idx - len(found_paths) - 1
                    selected_path, description = additional_paths[additional_idx]
                    print(f"선택된 경로: {selected_path} ({description})")
                    # 파일이 없어도 경로 반환 (생성 가능)
                    return [selected_path]
                
                else:
                    print(f"잘못된 번호입니다. 1-{total_options} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n사용자가 중단했습니다.")
                return None
    
    return found_paths


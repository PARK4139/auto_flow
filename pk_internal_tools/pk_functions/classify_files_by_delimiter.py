import shutil
import logging
from pathlib import Path
from typing import List

def _create_directory_structure_from_file_name(base_dir: Path, file_name: str, delimiter: str) -> Path:
    """
    Splits a file_name by a delimiter and creates a nested directory structure.
    The directory path is built from all parts of the file_name stem except the last one.
    """
    name_parts = Path(file_name).stem.split(delimiter)
    dir_parts = name_parts[:-1]

    if not dir_parts:
        return base_dir

    target_dir = base_dir
    for part in dir_parts:
        target_dir = target_dir / part
    
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

def classify_files_by_delimiter(source_files: List[str], destination_dir: str, delimiter: str = '_'):
    """
    Organizes a given list of files into a structured directory based on a delimiter.

    Args:
        source_files (List[str]): A list of absolute paths to the files to be organized.
        destination_dir (str): The root directory where the structured folders will be created.
        delimiter (str, optional): The character to split file_names by. Defaults to '_'.
    """
    logging.info(f"'{destination_dir}'에 '{delimiter}' 구분자를 기준으로 파일 정리를 시작합니다. 대상: {len(source_files)}개 파일")
    
    base_destination = Path(destination_dir)
    # Ensure the base destination directory exists to prevent errors.
    base_destination.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    
    for source_file_path in source_files:
        source_file = Path(source_file_path)
        if not source_file.is_file():
            logging.warning(f"경로가 파일이 아니거나 존재하지 않아 건너뜁니다: {source_file_path}")
            continue

        try:
            target_dir = _create_directory_structure_from_file_name(
                base_dir=base_destination,
                file_name=source_file.name,
                delimiter=delimiter
            )
            
            final_destination_path = target_dir / source_file.name
            shutil.move(str(source_file), str(final_destination_path))
            logging.info(f"이동: {source_file.name} -> {final_destination_path}")
            moved_count += 1
        
        except Exception as e:
            logging.error(f"'{source_file.name}' 파일 처리 중 오류 발생: {e}")

    logging.info(f"총 {moved_count}개의 파일 정리가 완료되었습니다.")
    return True

#!/usr/bin/env python3
"""
NUL 파일 자동 감지 및 제거 함수
- Windows 특수 파일 감지
- 자동 정리 및 Git에서 제거
- 프로젝트 품질 관리
"""

import os
import subprocess
from pathlib import Path
import logging


def detect_nul_files(project_root=None):
    """
    프로젝트에서 NUL 파일과 Windows 특수 파일을 감지하는 함수
    
    Args:
        project_root: 프로젝트 루트 경로 (기본값: 현재 디렉토리)
    
    Returns:
        list: 발견된 NUL 파일들의 경로 리스트
    """
    if project_root is None:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)
    
    logging.debug(f"프로젝트 루트에서 NUL 파일 검색 중: {project_root}")
    
    # Windows 특수 파일명들
    windows_reserved_names = {
        'nul', 'con', 'prn', 'aux', 'com1', 'com2', 'com3', 'com4',
        'lpt1', 'lpt2', 'lpt3', 'clock$', 'config$'
    }
    
    # Windows 시스템 파일들
    windows_system_files = {
        'Thumbs.db', 'Thumbs.db:encryptable', 'ehthumbs.db', 'ehthumbs_vista.db',
        'Desktop.ini', 'autorun.inf'
    }
    
    nul_files = []
    
    try:
        for root, dirs, files in os.walk(project_root):
            # 디렉토리명 검사
            for dir_name in dirs:
                if dir_name.lower() in windows_reserved_names:
                    nul_files.append(Path(root) / dir_name)
                    logging.debug(f"️  Windows 예약 디렉토리 발견: {Path(root) / dir_name}")
            
            # 파일명 검사
            for file_name in files:
                file_path = Path(root) / file_name
                
                # Windows 예약 파일명 검사
                if file_name.lower() in windows_reserved_names:
                    nul_files.append(file_path)
                    logging.debug(f"️  Windows 예약 파일 발견: {file_path}")
                
                # Windows 시스템 파일 검사
                elif file_name in windows_system_files:
                    nul_files.append(file_path)
                    logging.debug(f"️  Windows 시스템 파일 발견: {file_path}")
                
                # 빈 파일 검사 (0바이트)
                elif file_path.stat().st_size == 0:
                    nul_files.append(file_path)
                    logging.debug(f"️  빈 파일 발견: {file_path}")
                
                # NUL 문자 포함 파일명 검사
                elif '\x00' in file_name:
                    nul_files.append(file_path)
                    logging.debug(f"️  NUL 문자 포함 파일 발견: {file_path}")
    
    except Exception as e:
        logging.debug(f"NUL 파일 검색 중 오류 발생: {str(e)}")
    
    if nul_files:
        logging.debug(f"총 {len(nul_files)}개의 NUL 파일/디렉토리가 발견되었습니다.")
    else:
        logging.debug("NUL 파일이 발견되지 않았습니다.")
    
    return nul_files


def remove_nul_files(nul_files, dry_run=True):
    """
    NUL 파일들을 제거하는 함수
    
    Args:
        nul_files: 제거할 파일 경로 리스트
        dry_run: 실제 삭제하지 않고 미리보기만 (기본값: True)
    
    Returns:
        bool: 성공 여부
    """
    if not nul_files:
        logging.debug("제거할 NUL 파일이 없습니다.")
        return True
    
    logging.debug(f"NUL 파일 제거 시작 (dry_run: {dry_run})")
    
    success_count = 0
    error_count = 0
    
    for file_path in nul_files:
        try:
            if dry_run:
                logging.debug(f"[DRY RUN] 제거 예정: {file_path}")
                success_count += 1
            else:
                if file_path.is_file():
                    file_path.unlink()
                    logging.debug(f"️  파일 제거됨: {file_path}")
                elif file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                    logging.debug(f"️  디렉토리 제거됨: {file_path}")
                success_count += 1
                
        except Exception as e:
            logging.debug(f"제거 실패: {file_path} - {str(e)}")
            error_count += 1
    
    if dry_run:
        logging.debug(f"[DRY RUN] 총 {success_count}개 파일/디렉토리 제거 예정")
    else:
        logging.debug(f"총 {success_count}개 파일/디렉토리 제거 완료")
        if error_count > 0:
            logging.debug(f"️  {error_count}개 파일/디렉토리 제거 실패")
    
    return error_count == 0


def remove_nul_files_from_git(nul_files):
    """
    Git에서 NUL 파일들을 제거하는 함수
    
    Args:
        nul_files: Git에서 제거할 파일 경로 리스트
    
    Returns:
        bool: 성공 여부
    """
    if not nul_files:
        logging.debug("Git에서 제거할 NUL 파일이 없습니다.")
        return True
    
    logging.debug("Git에서 NUL 파일 제거 시작")
    
    success_count = 0
    error_count = 0
    
    for file_path in nul_files:
        try:
            # Git에서 파일 제거
            result = subprocess.run(
                ['git', 'rm', '--cached', str(file_path)],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            
            if result.returncode == 0:
                logging.debug(f"Git에서 제거됨: {file_path}")
                success_count += 1
            else:
                logging.debug(f"️  Git에서 제거 실패: {file_path} - {result.stderr}")
                error_count += 1
                
        except Exception as e:
            logging.debug(f"Git 제거 오류: {file_path} - {str(e)}")
            error_count += 1
    
    logging.debug(f"Git 제거 완료: {success_count}개 성공, {error_count}개 실패")
    
    return error_count == 0


def ensure_project_clean():
    """
    프로젝트를 깨끗하게 유지하는 메인 함수
    """
    logging.debug("프로젝트 NUL 파일 정리 시작")
    
    # n. NUL 파일 감지
    nul_files = detect_nul_files()
    
    if not nul_files:
        logging.debug("프로젝트가 이미 깨끗합니다!")
        return True
    
    # n. 미리보기 (dry run)
    logging.debug(" 제거 예정 파일들 미리보기:")
    remove_nul_files(nul_files, dry_run=True)
    
    # n. 사용자 확인
    logging.debug("️  위 파일들을 실제로 제거하시겠습니까?")
    logging.debug("계속하려면 'y'를 입력하세요:")
    
    # 실제 제거 실행
    remove_nul_files(nul_files, dry_run=False)
    
    # n. Git에서도 제거
    logging.debug(" Git에서 NUL 파일 제거 중...")
    remove_nul_files_from_git(nul_files)
    
    # n. 최종 확인
    final_check = detect_nul_files()
    if not final_check:
        logging.debug("프로젝트 정리 완료! 모든 NUL 파일이 제거되었습니다.")
    else:
        logging.debug(f"️  {len(final_check)}개 NUL 파일이 여전히 남아있습니다.")
    
    return len(final_check) == 0


# 사용 예제
if __name__ == "__main__":
    # 프로젝트 정리 실행
    ensure_project_clean()

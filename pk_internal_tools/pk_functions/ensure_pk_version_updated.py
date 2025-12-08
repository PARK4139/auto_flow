"""
pk_system 버전 업데이트 기능

오늘 날짜로 Git 태그를 생성하고 원격 저장소에 푸시합니다.
"""
import logging
import subprocess
from datetime import datetime
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import d_pk_root


def get_current_date_version() -> str:
    """오늘 날짜를 버전 형식으로 반환"""
    today = datetime.now()
    return f"{today.year}.{today.month}.{today.day}"


def get_version_from_git() -> str:
    """Git에서 현재 버전 가져오기"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--dirty"],
            capture_output=True,
            text=True,
            cwd=d_pk_root
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "unknown"
    except Exception as e:
        logging.warning(f"Git 버전 확인 실패: {e}")
        return "unknown"


def create_version_tag(version: str, message: str = None) -> bool:
    """Git 태그 생성"""
    tag_name = f"v{version}"
    
    # 이미 태그가 있는지 확인
    result = subprocess.run(
        ["git", "tag", "-l", tag_name],
        capture_output=True,
        text=True,
        cwd=d_pk_root
    )
    
    if result.stdout.strip():
        logging.warning(f"태그 {tag_name}가 이미 존재합니다.")
        logging.info(f"기존 태그를 삭제하고 새로 생성합니다.")
        subprocess.run(
            ["git", "tag", "-d", tag_name],
            cwd=d_pk_root
        )
    
    # 태그 메시지 생성
    if not message:
        message = f"Version {version}: Auto-updated to today's date"
    
    # 태그 생성
    try:
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", message],
            check=True,
            cwd=d_pk_root
        )
        logging.info(f"태그 {tag_name}가 생성되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"태그 생성 실패: {e}")
        return False


def push_version_tag(version: str) -> bool:
    """태그를 원격 저장소에 푸시"""
    tag_name = f"v{version}"
    try:
        result = subprocess.run(
            ["git", "push", "origin", tag_name],
            capture_output=True,
            text=True,
            cwd=d_pk_root
        )
        if result.returncode == 0:
            logging.info(f"태그 {tag_name}가 원격 저장소에 푸시되었습니다.")
            return True
        else:
            logging.error(f"태그 푸시 실패: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"태그 푸시 중 오류 발생: {e}")
        return False


@ensure_seconds_measured
def ensure_pk_version_updated():
    """
    pk_system 버전을 오늘 날짜로 업데이트합니다.
    
    - 오늘 날짜로 Git 태그 생성
    - 태그를 원격 저장소에 푸시
    - 업데이트된 버전 확인
    """
    func_n = get_caller_name()
    
    try:
        # 1. 오늘 날짜로 버전 생성
        version = get_current_date_version()
        logging.info(f"오늘 날짜 버전: {version}")
        
        # 2. 현재 버전 확인
        current_version = get_version_from_git()
        logging.info(f"현재 Git 버전: {current_version}")
        
        # 3. 태그 생성
        logging.info(f"버전 {version} 태그를 생성합니다.")
        if not create_version_tag(version):
            logging.error("태그 생성에 실패했습니다.")
            return
        
        # 4. 태그를 원격 저장소에 푸시
        logging.info(f"태그를 원격 저장소에 푸시합니다.")
        if not push_version_tag(version):
            logging.error("태그 푸시에 실패했습니다.")
            return
        
        # 5. 업데이트된 버전 확인
        updated_version = get_version_from_git()
        logging.info(f"업데이트된 Git 버전: {updated_version}")
        logging.info(f"버전 업데이트 완료: v{version}")
        
    except Exception as e:
        logging.error(f"버전 업데이트 중 오류 발생: {e}", exc_info=True)


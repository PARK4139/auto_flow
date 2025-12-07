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
    logging.debug("오늘 날짜 버전 생성 시작")
    today = datetime.now()
    version = f"{today.year}.{today.month}.{today.day}"
    logging.debug(f"생성된 버전: {version}")
    return version


def get_version_from_git() -> str:
    """Git에서 현재 버전 가져오기"""
    logging.debug("Git에서 현재 버전 가져오기 시작")
    command = ["git", "describe", "--tags", "--dirty"]
    logging.debug(f"실행할 명령어: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=d_pk_root,
            check=True
        )
        version = result.stdout.strip()
        logging.debug(f"Git describe 결과: {version}")
        if result.returncode == 0:
            return version
        logging.warning("Git describe 실행은 성공했으나, 리턴 코드가 0이 아닙니다.")
        return "unknown"
    except subprocess.CalledProcessError as e:
        logging.warning(f"Git 버전 확인 실패 (CalledProcessError): {e.stderr}")
        return "unknown"
    except FileNotFoundError:
        logging.error("Git 명령어를 찾을 수 없습니다. Git이 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
        return "unknown"
    except Exception as e:
        logging.warning(f"Git 버전 확인 중 예외 발생: {e}")
        return "unknown"


def create_version_tag(version: str, message: str = None) -> bool:
    """Git 태그 생성"""
    logging.debug(f"버전 {version}에 대한 Git 태그 생성 시작")
    tag_name = f"v{version}"
    
    # 이미 태그가 있는지 확인
    check_command = ["git", "tag", "-l", tag_name]
    logging.debug(f"태그 존재 확인 명령어: {' '.join(check_command)}")
    result = subprocess.run(
        check_command,
        capture_output=True,
        text=True,
        cwd=d_pk_root
    )
    
    if result.stdout.strip():
        logging.warning(f"태그 {tag_name}가 이미 존재합니다.")
        logging.info(f"기존 태그를 삭제하고 새로 생성합니다.")
        delete_command = ["git", "tag", "-d", tag_name]
        logging.debug(f"태그 삭제 명령어: {' '.join(delete_command)}")
        delete_result = subprocess.run(
            delete_command,
            cwd=d_pk_root,
            capture_output=True,
            text=True
        )
        if delete_result.returncode != 0:
            logging.error(f"기존 태그 삭제 실패: {delete_result.stderr}")
            return False
        logging.debug("기존 태그 삭제 완료")

    # 태그 메시지 생성
    if not message:
        message = f"Version {version}: Auto-updated to today's date"
    logging.debug(f"사용할 태그 메시지: {message}")
    
    # 태그 생성
    create_command = ["git", "tag", "-a", tag_name, "-m", message]
    logging.debug(f"태그 생성 명령어: {' '.join(create_command)}")
    try:
        create_result = subprocess.run(
            create_command,
            check=True,
            cwd=d_pk_root,
            capture_output=True,
            text=True
        )
        logging.info(f"태그 {tag_name}가 생성되었습니다.")
        logging.debug(f"태그 생성 결과: {create_result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"태그 생성 실패: {e.stderr}")
        return False


def push_version_tag(version: str) -> bool:
    """태그를 원격 저장소에 푸시"""
    logging.debug(f"버전 {version} 태그 푸시 시작")
    tag_name = f"v{version}"
    command = ["git", "push", "origin", tag_name]
    logging.debug(f"태그 푸시 명령어: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=d_pk_root,
            check=True
        )
        logging.info(f"태그 {tag_name}가 원격 저장소에 푸시되었습니다.")
        logging.debug(f"푸시 결과: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"태그 푸시 실패: {e.stderr}")
        # 푸시 실패 시, 원격에 강제 푸시를 시도할 수 있지만, 여기서는 실패로 처리.
        # 강제 푸시가 필요한 경우, '--force' 옵션을 추가해야 함.
        # 예: ["git", "push", "origin", tag_name, "--force"]
        # 여기서는 충돌 가능성을 알리기 위해 추가 로그를 남깁니다.
        if "rejected" in e.stderr:
            logging.warning("원격 저장소에서 태그 푸시가 거부되었습니다. 원격 태그가 로컬과 다를 수 있습니다.")
        return False
    except Exception as e:
        logging.error(f"태그 푸시 중 오류 발생: {e}", exc_info=True)
        return False


@ensure_seconds_measured
def ensure_pk_system_version_updated():
    """
    pk_system 버전을 오늘 날짜로 업데이트합니다.
    
    - 오늘 날짜로 Git 태그 생성
    - 태그를 원격 저장소에 푸시
    - 업데이트된 버전 확인
    """
    func_n = get_caller_name()
    logging.debug(f"'{func_n}' 함수 실행 시작")
    
    try:
        # 1. 오늘 날짜로 버전 생성
        logging.debug("1. 오늘 날짜로 버전 생성 단계")
        version = get_current_date_version()
        logging.info(f"오늘 날짜 버전: {version}")
        
        # 2. 현재 버전 확인
        logging.debug("2. 현재 Git 버전 확인 단계")
        current_version = get_version_from_git()
        logging.info(f"현재 Git 버전: {current_version}")
        
        # 3. 태그 생성
        logging.debug("3. 태그 생성 단계")
        logging.info(f"버전 {version} 태그를 생성합니다.")
        if not create_version_tag(version):
            logging.error("태그 생성에 실패했습니다. 프로세스를 중단합니다.")
            return
        
        # 4. 태그를 원격 저장소에 푸시
        logging.debug("4. 태그 푸시 단계")
        logging.info(f"태그를 원격 저장소에 푸시합니다.")
        if not push_version_tag(version):
            logging.error("태그 푸시에 실패했습니다. 롤백을 시도합니다.")
            # 롤백: 생성된 로컬 태그 삭제
            tag_name = f"v{version}"
            delete_command = ["git", "tag", "-d", tag_name]
            logging.debug(f"롤백: 로컬 태그 삭제 명령어: {' '.join(delete_command)}")
            subprocess.run(delete_command, cwd=d_pk_root)
            logging.info(f"롤백: 로컬 태그 {tag_name}가 삭제되었습니다.")
            return
        
        # 5. 업데이트된 버전 확인
        logging.debug("5. 최종 버전 확인 단계")
        updated_version = get_version_from_git()
        logging.info(f"업데이트된 Git 버전: {updated_version}")
        
        if f"v{version}" in updated_version:
            logging.info(f"버전 업데이트 성공: {updated_version}")
        else:
            logging.warning(f"버전 업데이트 후 확인 결과가 예상과 다릅니다. 최종 버전: {updated_version}")

    except Exception as e:
        logging.error(f"버전 업데이트 중 심각한 오류 발생: {e}", exc_info=True)
    finally:
        logging.debug(f"'{func_n}' 함수 실행 종료")


import logging
import traceback
from typing import Tuple, List, Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done

ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)


def ensure_remote_file_content_read(
    controller: PkRemoteTargetEngine,
    remote_file_path: str
) -> Tuple[bool, Optional[List[str]]]:
    """
    원격 타겟의 특정 파일 내용을 읽어옵니다.

    Args:
        controller (PkRemoteTargetEngine): 원격 타겟 컨트롤러 인스턴스.
        remote_file_path (str): 읽어올 원격 파일의 경로.

    Returns:
        Tuple[bool, Optional[List[str]]]: 파일 읽기 성공 여부와 파일 내용(줄바꿈으로 분리된 리스트).
                                            실패 시 (False, None) 반환.
    """
    try:
        logging.info(f"원격 파일 '{remote_file_path}' 내용 읽기 시도 중...")
        
        # 'cat' 명령어를 사용하여 파일 내용을 읽어옵니다.
        # 파일이 클 경우 문제가 될 수 있지만, 로그 파일이므로 괜찮을 것으로 가정합니다.
        cmd = f"cat {remote_file_path}"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=cmd,
            timeout_seconds=30,
            use_sudo=False  # 파일 읽기에는 sudo가 필요 없을 수 있음 (사용자 소유 파일의 경우)
        )

        if exit_code == 0:
            logging.info(f"원격 파일 '{remote_file_path}' 내용 읽기 성공.")
            return True, stdout
        else:
            logging.error(f"원격 파일 '{remote_file_path}' 내용 읽기 실패. Exit Code: {exit_code}")
            if stderr:
                for line in stderr:
                    logging.error(f"  {line}")
            return False, None

    except Exception as e:
        logging.error(f"원격 파일 내용 읽기 중 예외 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False, None

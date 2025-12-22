"""
명령어 처리 관련 함수들
명령어를 분석하고 실행합니다.
"""
import logging
import os

from pk_internal_tools.pk_functions.ensure_py_system_process_ran_by_pnx import ensure_py_system_process_ran_by_pnx
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_wsl_pk_distro_enabled import ensure_wsl_pk_distro_enabled
from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers
from pk_internal_tools.pk_kiria.pk_command_mapper import ProcessMatcher
from pk_internal_tools.pk_kiria.pk_kiri_state_utils import show_command_history, show_current_status
from pk_internal_tools.pk_objects.pk_texts import PK_WRAPPER_PREFIX
from pk_internal_tools.pk_objects.pk_kiri_state import KiriMode, KiriState
from pk_internal_tools.pk_objects.pk_texts import PkTexts

logger = logging.getLogger(__name__)


def try_execute_pk_process(command: str, state: KiriState) -> bool:
    """pk_system 프로세스 실행 시도"""
    try:
        # 실행 가능한 프로세스 목록 가져오기
        pk_wrappers = get_excutable_pk_wrappers()

        # 파일명만 추출하여 매칭
        import os
        for file_to_execute in pk_wrappers:
            file_name = os.path.basename(file_to_execute).replace('.py', '')
            if command.lower() == file_name.lower():
                try:
                    prefix = PK_WRAPPER_PREFIX
                    file_to_execute = file_to_execute
                    file_title = os.path.basename(file_to_execute)
                    file_title = file_title.removeprefix(prefix)
                    ensure_py_system_process_ran_by_pnx(file_to_execute, file_title)
                    logging.debug(f"{file_name} 완료")
                    return True
                except Exception as e:
                    logging.debug(f"{file_name} 실행 중 오류: {e}")
                    return True

        return False

    except Exception as e:
        logging.debug(f"️ 프로세스 실행 시도 중 오류: {e}")
        return False


def execute_pk_process(process_name: str, state: KiriState) -> bool:
    """PK 프로세스 실행"""
    try:
        # pk_ prefix 추가
        full_process_name = f"pk_{process_name}"

        # 실행 가능한 프로세스 목록에서 찾기
        pk_wrappers = get_excutable_pk_wrappers()

        import os
        for file_to_execute in pk_wrappers:
            file_name = os.path.basename(file_to_execute).replace('.py', '')
            if file_name == full_process_name:
                try:
                    prefix = PK_WRAPPER_PREFIX
                    file_title = os.path.basename(file_to_execute)
                    file_title = file_title.removeprefix(prefix)
                    ensure_py_system_process_ran_by_pnx(file_to_execute, file_title)
                    logging.debug(f"{process_name} 실행 완료")
                    return True
                except Exception as e:
                    logging.debug(f"{process_name} 실행 중 오류: {e}")
                    return True

        logging.debug(f"{process_name} 프로세스를 찾을 수 없습니다.")
        return False

    except Exception as e:
        logging.debug(f"프로세스 실행 중 오류: {e}")
        return False


def suggest_and_execute_process(user_command: str, state: KiriState) -> bool:
    """유사한 프로세스 제안 및 실행"""
    try:
        # 유사한 프로세스 찾기
        similar_processes = state.process_matcher.find_similar_processes(user_command, threshold=0.1)

        if not similar_processes:
            logging.debug(f"'{user_command}'와 유사한 프로세스를 찾을 수 없습니다.")
            return False

        # 상위 5개만 표시
        top_similar = similar_processes[:5]

        logging.debug(f"'{user_command}'와 유사한 프로세스들:")
        for i, (process_name, similarity) in enumerate(top_similar, 1):
            similarity_percent = similarity * 100
            logging.debug(f"{i}. {process_name} (유사도: {similarity_percent:.1f}%)")

        # 사용자 선택 받기
        logging.debug("실행할 프로세스 번호를 선택하세요 (0: 취소):")
        try:
            choice = input("선택=").strip()
            if not choice or choice == "0":
                logging.debug("취소되었습니다.")
                return True

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(top_similar):
                selected_process = top_similar[choice_idx][0]

                # 실행 확인
                logging.debug(f"'{selected_process}' 프로세스를 실행하시겠습니까? (y/n):")
                confirm = input("확인=").strip().lower()

                if confirm in ['y', 'yes', '예', '네']:
                    # 프로세스 실행
                    return execute_pk_process(selected_process, state)
                else:
                    logging.debug("실행이 취소되었습니다.")
                    return True
            else:
                logging.debug("잘못된 선택입니다.")
                return True

        except ValueError:
            logging.debug("숫자를 입력해주세요.")
            return True
        except KeyboardInterrupt:
            logging.debug("취소되었습니다.")
            return True

    except Exception as e:
        logging.debug(f"프로세스 제안 중 오류: {e}")
        return False


def process_command(command: str, state: KiriState) -> bool:
    """명령어 처리 - 개선된 에러 처리"""
    command = command.lower()

    try:
        # 마이크 상태 확인 명령어
        if command in ["check mic", "마이크 확인"]:
            if state.check_microphone_status():
                logging.debug("마이크가 정상적으로 연결되어 있습니다.")
                if state.current_mode == KiriMode.KEYBOARD_CONVERSATION:
                    logging.debug("'mode voice' 명령어로 음성 대화 모드로 전환할 수 있습니다.")
            else:
                logging.debug("마이크가 연결되지 않았습니다.")
            return True

        # 모드 전환 명령어들
        if command in ["mode keyboard", "keyboard mode", "키보드 모드", "mode cli", "cli mode", "텍스트 모드"]:
            state.switch_mode(KiriMode.KEYBOARD_CONVERSATION)
            return True
        elif command in ["mode voice", "voice mode", "음성 모드", "음성 대화 모드"]:
            if state.microphone_available:
                state.switch_mode(KiriMode.VOICE_CONVERSATION)
            else:
                logging.debug("마이크가 연결되지 않아 음성 대화 모드로 전환할 수 없습니다.")
            return True
        elif command in ["mode hybrid", "hybrid mode", "하이브리드 모드"]:
            if state.microphone_available:
                state.switch_mode(KiriMode.HYBRID)
            else:
                logging.debug("마이크가 연결되지 않아 하이브리드 모드로 전환할 수 없습니다.")
            return True
        elif command in ["mode silent", "silent mode", "무음 모드"]:
            state.switch_mode(KiriMode.SILENT)
            return True
        elif command in ["mode debug", "debug mode", "디버그 모드"]:
            state.switch_mode(KiriMode.DEBUG)
            return True

        # 종료 명령어
        if command in ["quit", "exit", "종료", "나가기"]:
            response = f"{PkTexts.QUIT_MESSAGE}"
            if state.current_mode != KiriMode.SILENT:
                ensure_spoken(response)
            logging.debug(f"{PkTexts.QUITTING}...")
            return False
        elif command in ["wsl 활성화"]:
            if not ensure_wsl_pk_distro_enabled():
                raise RuntimeError("WSL 배포판 설치/이름 변경에 실패했습니다.")
        elif command in ["history", "히스토리"]:
            show_command_history(state)
        elif command in ["status", "상태"]:
            show_current_status(state)
        elif command == "":
            if state.current_mode != KiriMode.SILENT:
                logging.debug(f"{PkTexts.WHAT_CAN_I_HELP}? (help 입력시 명령어 확인)")
        else:
            # 동적 매핑 정보 항상 출력
            state.process_matcher.print_dynamic_mapping(command)

            # n. 동적 매핑 우선 실행
            dynamic_matches = state.process_matcher.find_dynamic_matches(command)
            if dynamic_matches:
                logging.debug(f"동적으로 매핑된 함수: {dynamic_matches}")
                # 실제 실행은 나중에 구현, 일단 매핑 정보만 출력
                return True

            # n. 정확한 프로세스명 매칭 시도
            if try_execute_pk_process(command, state):
                return True

            # n. 유사도 기반 제안
            if suggest_and_execute_process(command, state):
                return True

            # 매칭되지 않은 경우
            response = f"'{command}' {PkTexts.UNKNOWN_COMMAND}. 자연어로 프로세스를 설명해보세요."
            if state.current_mode != KiriMode.SILENT:
                ensure_spoken(response)
            logging.debug(f"{response}")

        return True

    except Exception as e:
        error_msg = f" 명령어 처리 중 오류: {e}"
        logging.debug(error_msg)
        if state.current_mode != KiriMode.SILENT:
            ensure_spoken(f"{PkTexts.ERROR_OCCURRED}")
        return True


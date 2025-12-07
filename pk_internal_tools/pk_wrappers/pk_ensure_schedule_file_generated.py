import datetime
import logging
import sys
from pathlib import Path

# pk_internal_tools 모듈을 찾을 수 있도록 프로젝트 루트를 시스템 경로에 추가합니다.
try:
    # 이 파일은 pk_internal_tools/pk_wrappers/ 에 위치합니다.
    project_root = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(project_root))
except NameError:
    # 대화형 환경 등 __file__ 변수가 없는 경우를 위한 대비책
    sys.path.append(str(Path.cwd()))

# --- 로깅 설정 --- #
# 프로젝트의 표준 로깅 초기화 함수를 사용하려 시도합니다.
# 실패 시, 기본적인 로깅 설정을 사용합니다.
try:
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
except ImportError:
    def ensure_pk_log_initialized(file):
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s')
        logging.info("경고: 표준 로깅 초기화 함수를 찾지 못해 기본 설정을 사용합니다.")


def main():
    """
    fzf를 통해 사용자로부터 연도를 입력받아, 해당 연도의 일정 생성 함수를 호출하는 메인 함수.
    """
    # 표준 로깅을 초기화합니다.
    ensure_pk_log_initialized(__file__)

    try:
        # 필요한 핵심 함수들을 임포트합니다.
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
        from pk_internal_tools.pk_functions.ensure_generate_schedule_functions_for_year import ensure_generate_schedule_functions_for_year
    except ImportError as e:
        logging.error(f"필요한 함수를 임포트하는 데 실패했습니다: {e}")
        logging.error("프로젝트 경로가 올바른지, 함수 파일이 존재하는지 확인해주세요.")
        return

    # fzf에 표시할 연도 목록 생성 (현재 연도 기준 -5년 ~ +5년)
    current_year = datetime.date.today().year
    years = [str(y) for y in range(current_year - 5, current_year + 6)]

    # fzf를 통해 사용자에게 연도 선택을 요청합니다.
    selected_year_str = ensure_value_completed_2025_10_12_0000(
        key_name="일정 파일을 생성할 연도를 선택하세요",
        options=years,
        default_value=str(current_year) # pk_option: 기본값으로 현재 연도 설정
    )

    if not selected_year_str:
        logging.warning("연도를 선택하지 않았습니다. 작업을 취소합니다.")
        return

    try:
        selected_year = int(selected_year_str)
        logging.info(f"{selected_year}년 일정 파일 생성을 시작합니다.")
        
        # 연도를 인자로 전달하여 일정 파일 생성 함수를 호출합니다.
        success = ensure_generate_schedule_functions_for_year(selected_year)
        
        if success:
            logging.info(f"{selected_year}년 일정 파일 생성이 완료되었습니다.")
        else:
            logging.error(f"{selected_year}년 일정 파일 생성에 실패했습니다.")

    except ValueError:
        logging.error(f"잘못된 연도 형식입니다: '{selected_year_str}'")
    except Exception as e:
        logging.error(f"작업 중 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()

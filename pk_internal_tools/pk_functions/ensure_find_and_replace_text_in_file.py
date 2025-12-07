import logging
import re
from pathlib import Path

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE_SHORT, PK_UNDERLINE_HALF, ANSI_COLOR_MAP

def find_and_replace_text_in_file(file_path: str, old_text: str, new_text: str, case_sensitive: bool = False):
    """
    지정된 파일 내에서 텍스트를 찾아 교체합니다.

    Args:
        file_path (str): 대상 파일의 경로.
        old_text (str): 찾을 텍스트.
        new_text (str): 교체할 텍스트.
        case_sensitive (bool): 대소문자를 구분하여 교체할지 여부. 기본값은 False.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        logging.warning(f"파일을 찾을 수 없습니다: {file_path}")
        return

    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # re.escape를 사용하여 old_text가 정규식으로 해석되지 않도록 방지
        # 그러나 old_text가 사용자의 입력이므로, 사용자가 정규식으로 해석되기를 원할 수도 있음.
        # 여기서는 단순 텍스트 교체로 가정하고 re.escape를 사용.
        # 사용자가 정규식을 원한다면, 별도의 옵션을 추가해야 함.
        # 일단은 단순 텍스트 교체에 집중.
        
        # 줄바꿈 문자를 포함하여 정확히 일치하는 텍스트를 찾기 위해 re.DOTALL 사용
        # content = re.sub(re.escape(old_text), new_text, content, flags=flags | re.DOTALL)
        
        # 단순히 문자열 교체로 처리 (re.sub는 re.escape가 필요하지만 str.replace는 필요 없음)
        if not case_sensitive:
            # 대소문자 구분 없이 교체하려면, 먼저 패턴을 컴파일하고 모든 일치 항목을 찾은 다음 교체
            # 이는 str.replace가 대소문자를 구분하기 때문.
            # 하지만 여기서는 re.sub를 사용하는 것이 더 적합.
            
            # re.compile을 사용하여 효율성을 높이고, flags 설정
            pattern = re.compile(re.escape(old_text), flags)
            new_content = pattern.sub(new_text, content)
        else:
            new_content = content.replace(old_text, new_text)

        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            logging.debug(f"{PK_UNDERLINE_SHORT} 파일 내용 교체 완료 {PK_UNDERLINE_HALF}")
            logging.debug(f"{ANSI_COLOR_MAP['BRIGHT_GREEN']}파일: {file_path}{ANSI_COLOR_MAP['RESET']}")
            logging.debug(f"{ANSI_COLOR_MAP['YELLOW']}기존 텍스트: {old_text}{ANSI_COLOR_MAP['RESET']}")
            logging.debug(f"{ANSI_COLOR_MAP['CYAN']}새 텍스트: {new_text}{ANSI_COLOR_MAP['RESET']}")
        else:
            logging.debug(f"파일 내용에 변화 없음: {file_path}")

    except Exception as e:
        logging.error(f"파일 텍스트 교체 중 오류 발생 ({file_path}): {e}")

if __name__ == "__main__":
    # 테스트 코드를 직접 작성하지 않습니다.
    # 이 파일은 함수/모듈 파일(래퍼가 아닌 파일)이므로 테스트용 `if __name__ == '__main__':` 블록을 작성하지 않습니다.
    # 로깅 초기화(`ensure_pk_log_initialized`)는 실행 진입점인 래퍼 스크립트에서만 호출합니다.
    pass

import datetime
import textwrap
from pathlib import Path
import logging

def ensure_generate_schedule_functions_for_year(year: int):
    """
    지정된 연도의 일정 파일을 생성하고, 그 안에 365/366일치 날짜별 메소드를 포함한
    '일정{year}' 클래스의 전체 코드를 작성합니다.
    TODO : 4분기 단위 일정
    """
    try:
        # 이 파일의 위치를 기준으로 부모 디렉토리를 참조하여 목표 경로를 설정합니다.
        target_dir = Path(__file__).resolve().parent.parent / "pk_memo"
    except NameError:
        # 대화형 환경 등 __file__ 변수가 없는 경우를 위한 대비책
        target_dir = Path("./pk_internal_tools/pk_memo")

    target_file = target_dir / f"일정{year}.py"

    logging.info(f"'{target_file}' 파일 생성을 시작합니다...")

    class_code = "import textwrap\n\n"
    class_code += f"class 일정{year}:\n"
    class_code += f"    \"\"\"{year}년 일정을 관리하는 클래스\"\"\n\n"

    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    
    korean_weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    
    current_date = start_date
    while current_date <= end_date:
        y, m, d = current_date.year, current_date.month, current_date.day
        weekday_str = korean_weekdays[current_date.weekday()]
        
        method_name = f"일정_{y}_{m:02d}_{d:02d}_{weekday_str}"
        
        method_code = textwrap.dedent(f"""
            def {method_name}(self):
                \"\"\" {y}년 {m}월 {d}일 ({weekday_str}) 일정 \"\"\" 
                return textwrap.dedent(f'''
                    # {y}-{m:02d}-{d:02d} ({weekday_str})
                    
                ''')
        """ 
        )
        
        indented_method_code = textwrap.indent(method_code, "    ")
        class_code += indented_method_code + "\n\n"
        
        current_date += delta

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(class_code)
        logging.info(f"성공적으로 '{target_file}' 파일을 생성했습니다.")
        return True
    except IOError as e:
        logging.error(f"파일을 작성하는 중 오류가 발생했습니다: {e}")
        return False
import logging
import re
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_process_killed_by_window_title import ensure_process_killed_by_window_title
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
from pk_internal_tools.pk_functions.ensure_window_to_front_2025_11_23 import ensure_window_to_front_2025_11_23
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE


def _get_process_name_from_wrapper(wrapper_path: Path) -> str:
    """래퍼 파일명에서 프로세스 이름을 추출합니다."""
    # e.g., pk_ensure_my_process.py -> my_process
    match = re.match(r"pk_ensure_(.+)\.py", wrapper_path.name)
    if match:
        return match.group(1).replace("_", " ")
    # Fallback to just the file stem
    return wrapper_path.stem


def ensure_pk_process_control():
    """
    pk_process 제어 기능
    
    - fzf에서 pk_process를 선택받음
    - fzf에서 액션을 선택받음 (실행 or 종료 | 창앞으로이동)
    - pk_process 액션을 수행
    - 래퍼 파일명은 pk_ensure_~ 패턴
    - get_window_titles() 순환하며 fzf에 리스트업
    - 래퍼 파일명과 같은게 있다면 상태를 실행중으로 판단
    - fzf list output format: {window title}(실행중)
    """
    func_n = get_caller_name()
    
    try:
        # 1. pk_ensure_ 패턴의 래퍼 파일들 찾기
        wrappers = [f for f in Path(d_pk_wrappers).glob("pk_ensure_*.py") if f.is_file()]
        if not wrappers:
            logging.warning("pk_wrappers에 제어할 프로세스가 없습니다.")
            return
        
        # 2. 현재 실행 중인 창 제목들 가져오기
        all_titles = get_window_titles()
        
        # 3. 프로세스 상태 맵 및 fzf 옵션 생성
        process_status_map = {}
        fzf_options = []
        
        for wrapper in wrappers:
            process_name_long = wrapper.stem  # pk_ensure_xxx
            process_name_short = _get_process_name_from_wrapper(wrapper)  # xxx
            
            # 래퍼 파일명과 같은 창 제목이 있는지 확인
            running_window = next((title for title in all_titles if process_name_long in title), None)
            
            if running_window:
                # 실행 중: {window title}(실행중) 형식
                display_name = f"{running_window}(실행중)"
                process_status_map[display_name] = {
                    "status": "running",
                    "wrapper_path": wrapper,
                    "window_title": running_window,
                    "process_name": process_name_short,
                    "process_name_long": process_name_long
                }
            else:
                # 종료 중: 래퍼 파일명만 표시
                display_name = process_name_long
                process_status_map[display_name] = {
                    "status": "stopped",
                    "wrapper_path": wrapper,
                    "window_title": None,
                    "process_name": process_name_short,
                    "process_name_long": process_name_long
                }
            
            fzf_options.append(display_name)
        
        # 4. fzf에서 pk_process 선택
        selected_display_name = ensure_value_completed_2025_11_11(
            key_name="pk_process",
            func_n=func_n,
            guide_text="제어할 pk_process를 선택하세요:",
            options=sorted(fzf_options)
        )
        
        if not selected_display_name:
            logging.info("프로세스를 선택하지 않았습니다.")
            return
        
        selected_process = process_status_map.get(selected_display_name)
        if not selected_process:
            logging.error("잘못된 선택입니다.")
            return
        
        # 5. fzf에서 액션 선택 (실행 or 종료 | 창앞으로이동)
        # 모든 액션을 표시하되, 상태에 따라 적절한 액션만 활성화
        if selected_process["status"] == "running":
            # 실행 중일 때: 종료 | 창앞으로이동
            action_options = ["종료", "창앞으로이동"]
        else:
            # 종료 중일 때: 실행
            action_options = ["실행"]
        
        selected_action = ensure_value_completed_2025_11_11(
            key_name="pk_process_action",
            func_n=func_n,
            guide_text=f"'{selected_process['process_name']}'에 대한 액션을 선택하세요:",
            options=action_options
        )
        
        if not selected_action:
            logging.info("액션을 선택하지 않았습니다.")
            return
        
        # 6. pk_process 액션 수행
        if selected_action == "실행":
            wrapper_path = selected_process['wrapper_path']
            # 래퍼 파일명을 활용해서 title을 replace
            window_title = selected_process['process_name_long']
            cmd = f'start "{window_title}" "{F_UV_PYTHON_EXE}" "{wrapper_path}"'
            logging.info(f"프로세스 실행: {cmd}")
            ensure_command_executed(cmd, mode='a')
            logging.info(f"'{selected_process['process_name']}' 프로세스를 실행했습니다.")
        
        elif selected_action == "종료":
            window_title = selected_process['window_title']
            logging.info(f"프로세스 종료: {window_title}")
            ensure_process_killed_by_window_title(window_title)
            logging.info(f"'{selected_process['process_name']}' 프로세스를 종료했습니다.")
        
        elif selected_action == "창앞으로이동":
            window_title = selected_process['window_title']
            logging.info(f"창 앞으로 이동: {window_title}")
            # ensure_window_to_front_2025_11_23은 window_title_seg를 받음
            ensure_window_to_front_2025_11_23(window_title_seg=window_title)
            logging.info(f"'{selected_process['process_name']}' 창을 앞으로 가져왔습니다.")
    
    except Exception as e:
        logging.error(f"pk_process 제어 중 오류 발생: {e}", exc_info=True)


def ensure_pk_process_controller_executed():
    """
    레거시 함수명 유지 (하위 호환성)
    ensure_pk_process_control()을 호출합니다.
    """
    ensure_pk_process_control()


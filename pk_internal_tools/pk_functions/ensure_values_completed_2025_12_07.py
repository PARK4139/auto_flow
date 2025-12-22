import logging
import os
import subprocess
import textwrap

from pk_internal_tools.pk_functions.get_ensure_value_complete_shortcut_guide_text import get_ensure_value_complete_shortcut_guide_text
from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
from pk_internal_tools.pk_functions.get_file_id import get_file_id
from pk_internal_tools.pk_functions.get_fzf_executable_command import get_fzf_executable_command
from pk_internal_tools.pk_functions.get_hashed_items import get_hashed_items
from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pk_fzf_options import get_pk_fzf_options
from pk_internal_tools.pk_functions.get_pk_label_by_via import get_pk_label_by_via
from pk_internal_tools.pk_functions.get_str_removed_bracket_hashed_prefix import get_str_removed_bracket_hashed_prefix
from pk_internal_tools.pk_functions.get_user_input_guide_text import get_user_input_guide_text
from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
from pk_internal_tools.pk_objects.pk_etc import PK_POINTER_COLOR, PK_FOOTER_COLOR, PK_FG_ACTIVE_COLOR, PK_HL_ACTIVE_COLOR, PK_HL_COLOR, PK_PROMPT_COLOR, PK_QUERY_COLOR, PK_SPINNER_COLOR
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def ensure_values_completed_2025_12_07(
        key_name: str,
        options: list[str],
        func_n: str = None,
        multi_select: bool = True,
        guide_text: str = None,
        history_reset: bool = False,
) -> list[str]:
    """
    fzf 외부 명령어를 사용하여 사용자에게 다중 선택 가능한 목록을 제시하고,
    선택된 값들을 리스트로 반환합니다.
    history 기능이 포함되어 있어 이전 선택값을 자동으로 불러오고 저장합니다.
    
    Args:
        key_name: 선택 메뉴의 이름/제목
        options: 선택 가능한 옵션 목록
        func_n: 호출 함수 이름 (history 파일 ID 생성에 사용, None이면 자동 감지)
        multi_select: 다중 선택 모드 여부 (기본값: True)
        guide_text: 사용자 가이드 텍스트 (선택사항)
        history_reset: history 파일 초기화 여부 (기본값: False)
    
    Returns:
        list[str]: 선택된 값들의 리스트 (선택 취소 시 빈 리스트)
    """
    # file_id 생성 (history 파일 식별에 사용)
    file_id = get_file_id(key_name, func_n)

    # history 파일 경로 가져오기
    f_historical = get_history_file_path(file_id=file_id)

    # history_reset이 True인 경우 history 파일 초기화
    if history_reset:
        if os.path.exists(f_historical):
            try:
                with open(f_historical, 'w', encoding='utf-8') as f:
                    f.write('')
                logging.info(f"History file has been reset: {f_historical}")
            except IOError as e:
                logging.error(f"Failed to reset history file {f_historical}: {e}")

    # history에서 이전 값들 가져오기
    historical_values = get_values_from_history_file(f_historical=f_historical)

    # options와 history 값 병합
    options = get_list_calculated(origin_list=options or [], plus_list=historical_values)
    options = get_list_calculated(origin_list=options, dedup=True)  # 중복 제거

    logging.debug(f'''file_id={file_id} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    # 마지막 선택값 가져오기 (fzf 쿼리로 사용)
    last_selected = get_last_selected(f_historical)
    logging.debug(f'''last_selected={last_selected} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    # 마지막 선택값이 있으면 옵션 맨 앞에 추가
    if last_selected.strip() != "":
        options = get_list_calculated(origin_list=[last_selected], plus_list=options)
        options = get_list_calculated(origin_list=options, dedup=True)  # 중복 제거

    if not options:
        return []

    # fzf 명령어 경로 확인
    fzf_executable_command = get_fzf_executable_command()

    # guide_text 출력 (있는 경우)
    if guide_text:
        logging.info(guide_text)

    try:
        import platform  # try 블록 안에 필요한 import 이동 (platform 모듈은 상단으로 옮겨야 함)

        # fzf 인자 구성
        fzf_args = [str(fzf_executable_command)] + get_pk_fzf_options(prompt_text=f"{key_name}> ")

        # --print0 옵션 추가
        if "--print0" not in fzf_args:
            fzf_args.append("--print0")

        # 다중 선택 모드 설정
        if multi_select:
            # --no-multi를 제거하고 --multi를 추가
            if "--no-multi" in fzf_args:
                fzf_args.remove("--no-multi")
            if "--multi" not in fzf_args:
                fzf_args.append("--multi")

        # 마지막 선택값을 초기 쿼리로 설정
        if last_selected.strip():
            fzf_args.append("--query")
            fzf_args.append(last_selected.strip())

        # 더블클릭으로 클립보드에 복사 옵션 통합
        double_click_bind_option = ""
        if platform.system() == "Windows":
            double_click_bind_option = "double-click:execute-silent(echo {} | clip.exe)"
        else:
            double_click_bind_option = "double-click:execute-silent(echo {} | xclip -selection clipboard 2>/dev/null || echo {} | pbcopy 2>/dev/null || true)"

        bind_index = -1
        existing_bind_value = ""
        for i, arg in enumerate(fzf_args):
            if arg == "--bind":
                bind_index = i
                existing_bind_value = fzf_args[i + 1]
                break

        if bind_index != -1:
            # 기존 --bind 옵션에 double-click 바인딩 추가
            new_bind_value = f"{existing_bind_value},{double_click_bind_option}"
            fzf_args[bind_index + 1] = new_bind_value
        else:
            # --bind 옵션이 없으면 새로 추가
            fzf_args.append("--bind")
            fzf_args.append(double_click_bind_option)

        # 푸터 텍스트 구성
        pk_label = get_pk_label_by_via(file_id)
        user_input_guide_text = get_user_input_guide_text(pk_label)
        ensure_value_complete_shortcut_guide_text = get_ensure_value_complete_shortcut_guide_text(multi_select)
        footer_guide = textwrap.dedent(rf'''
            # 사용자 입력 {PkTexts.TUTORIAL}
            {textwrap.dedent(user_input_guide_text).strip()}

            # 단축키 {PkTexts.TUTORIAL}
            {textwrap.dedent(ensure_value_complete_shortcut_guide_text).strip()}
        ''').strip()
        fzf_args.append("--footer")
        fzf_args.append(footer_guide)
        fzf_args.append(f"--color=query:{PK_QUERY_COLOR},spinner:{PK_SPINNER_COLOR},prompt:{PK_PROMPT_COLOR},pointer:{PK_POINTER_COLOR},hl:{PK_HL_COLOR},hl+:{PK_HL_ACTIVE_COLOR},fg+:{PK_FG_ACTIVE_COLOR},footer:{PK_FOOTER_COLOR}")

        env_vars = os.environ.copy()
        env_vars['PYTHONIOENCODING'] = 'utf-8'
        env_vars['LANG'] = 'ko_KR.UTF-8'
        env_vars['LC_ALL'] = 'ko_KR.UTF-8'

        # Apply hashing just before sending to fzf input
        hashed_options = get_hashed_items(options)
        fzf_input = '\n'.join(hashed_options)

        proc = subprocess.Popen(
            fzf_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env_vars,
        )

        # 사용자 입력 대기 (UTF-8로 인코딩된 문자열 전달)
        out, err = proc.communicate(input=fzf_input)

        # 선택된 값들 파싱
        selected_values = out.strip('\0').split('\0')
        selected_values = [v for v in selected_values if v]

        # 선택된 값에서 해시 제거
        selected_values = [get_str_removed_bracket_hashed_prefix(v) for v in selected_values]

        # fzf 프로세스 종료 코드 확인 및 결과 반환
        if proc.returncode == 0:  # 성공적으로 종료
            # 선택된 값들을 history에 저장 (성공적으로 선택되었을 때만)
            if selected_values:
                options_to_save = get_list_calculated(origin_list=selected_values, plus_list=options)
                options_to_save = get_list_calculated(origin_list=options_to_save, dedup=True)
                set_values_to_historical_file(f_historical=f_historical, values=options_to_save)
                logging.debug(f'''len(options_to_save)={len(options_to_save)} {'''%%%FOO%%% ''' if QC_MODE else ''}''')
            return selected_values
        elif proc.returncode == 130:  # User cancelled (Ctrl+C or ESC)
            logging.info("fzf 선택이 사용자에 의해 취소되었습니다.")
            return []
        else:  # 그 외 오류
            logging.error(f"fzf 실행 중 오류 발생 (코드: {proc.returncode}): {err}")
            return []

    except Exception as e:
        logging.error(f"fzf 다중 선택 처리 중 예상치 못한 오류 발생: {e}", exc_info=True)
        return []

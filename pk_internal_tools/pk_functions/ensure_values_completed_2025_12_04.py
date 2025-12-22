import logging
import os
import subprocess
import textwrap

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed  # Fallback
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_ensure_value_complete_shortcut_guide_text import get_ensure_value_complete_shortcut_guide_text
from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
from pk_internal_tools.pk_functions.get_file_id import get_file_id
from pk_internal_tools.pk_functions.get_fzf_executable_command import get_fzf_executable_command
from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pk_label_by_via import get_pk_label_by_via
from pk_internal_tools.pk_functions.get_user_input_guide_text import get_user_input_guide_text
from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
from pk_internal_tools.pk_objects.pk_etc import PK_POINTER_COLOR, PK_PROMPT_COLOR, PK_FOOTER_COLOR, PK_HL_COLOR, PK_FG_ACTIVE_COLOR, PK_HL_ACTIVE_COLOR, PK_QUERY_COLOR, PK_SPINNER_COLOR, PK_POINTER_TEXT
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def ensure_values_completed_2025_12_04(
        key_name: str,
        options: list[str],
        func_n: str = None,
        multi_select: bool = False,
        guide_text: str = None,
        history_reset: bool = False,
) -> list[str]:
    """
    fzf 외부 명령어를 사용하여 사용자에게 다중 선택 가능한 목록을 제시하고,
    선택된 값들을 리스트로 반환합니다.
    multi_select가 False인 경우 단일 선택 모드로 동작합니다.
    history 기능이 포함되어 있어 이전 선택값을 자동으로 불러오고 저장합니다.
    
    Args:
        key_name: 선택 메뉴의 이름/제목
        options: 선택 가능한 옵션 목록
        func_n: 호출 함수 이름 (history 파일 ID 생성에 사용, None이면 자동 감지)
        multi_select: 다중 선택 모드 여부 (기본값: False)
        guide_text: 사용자 가이드 텍스트 (선택사항)
        history_reset: history 파일 초기화 여부 (기본값: False)
    
    Returns:
        list[str]: 선택된 값들의 리스트 (선택 취소 시 빈 리스트)
    """
    # func_n이 제공되지 않은 경우 자동 감지
    if func_n is None:
        func_n = get_caller_name()

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

    logging.debug(f'''file_id={file_id} {"%%%FOO%%% " if QC_MODE else ""}''')

    # 마지막 선택값 가져오기 (fzf 쿼리로 사용)
    last_selected = get_last_selected(f_historical)
    logging.debug(f'''last_selected={last_selected} {"%%%FOO%%% " if QC_MODE else ""}''')

    # 마지막 선택값이 있으면 옵션 맨 앞에 추가
    if last_selected.strip() != "":
        options = get_list_calculated(origin_list=[last_selected], plus_list=options)
        options = get_list_calculated(origin_list=options, dedup=True)  # 중복 제거

    if not options:
        return []

    # fzf 명령어 경로 확인
    fzf_executable_command = get_fzf_executable_command()
    if not fzf_executable_command:
        logging.error("fzf 명령어를 찾을 수 없습니다. fzf가 설치되어 있고 PATH에 있는지 확인해주세요.")
        logging.warning("fzf를 찾을 수 없어 단일 선택 모드로 대체합니다.")
        # Fallback to the project-specific single-select function
        selected = ensure_value_completed(key_name=key_name, options=options, func_n=func_n)
        # history에 저장
        if selected:
            options_to_save = get_list_calculated(origin_list=[selected], plus_list=options)
            options_to_save = get_list_calculated(origin_list=options_to_save, dedup=True)
            set_values_to_historical_file(f_historical=f_historical, values=options_to_save)
        return [selected] if selected else []

    # guide_text 출력 (있는 경우)
    if guide_text:
        logging.info(guide_text)

    try:
        # fzf 인자 구성
        fzf_args = [
            "--ansi",
            "--prompt", f"{key_name}> ",
            "--print0",
            f"--pointer={PK_POINTER_TEXT}",  
            f"--color=query:{PK_QUERY_COLOR},spinner:{PK_SPINNER_COLOR},prompt:{PK_PROMPT_COLOR},pointer:{PK_POINTER_COLOR},hl:{PK_HL_COLOR},hl+:{PK_HL_ACTIVE_COLOR},fg+:{PK_FG_ACTIVE_COLOR}",
            "--height=40%",
            "--layout=reverse",
            "--border",
        ]

        # 다중 선택 모드 설정
        if multi_select:
            fzf_args.insert(1, "--multi")  # --multi 옵션을 --ansi 다음 또는 적절한 위치에 삽입

            # 멀티 선택 모드에서만 "select-all" 바인딩 추가
            fzf_args.append("--bind")
            fzf_args.append("alt-a:select-all")

        # 마지막 선택값을 초기 쿼리로 설정
        if last_selected.strip():
            fzf_args.append("--query")
            fzf_args.append(last_selected.strip())

        # 더블클릭으로 클립보드에 복사 (Windows)
        import platform
        if platform.system() == "Windows":
            # Windows: clip.exe 사용
            fzf_args.append("--bind")
            fzf_args.append("double-click:execute-silent(echo {} | clip.exe)")
        else:
            # Linux/Mac: xclip 또는 pbcopy 사용
            fzf_args.append("--bind")
            fzf_args.append("double-click:execute-silent(echo {} | xclip -selection clipboard 2>/dev/null || echo {} | pbcopy 2>/dev/null || true)")

        # 푸터 텍스트 구성
        # 단축키 ALT-A 관련 안내 추가
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

        # fzf 실행
        cmd = fzf_executable_command + fzf_args
        process = subprocess.run(
            cmd,
            input='\n'.join(options).encode('utf-8'),
            capture_output=True,
            check=True
        )

        # 선택된 값들 파싱
        selected_values = process.stdout.decode('utf-8').strip('\0').split('\0')
        selected_values = [v for v in selected_values if v]

        # 선택된 값들을 history에 저장
        if selected_values:
            options_to_save = get_list_calculated(origin_list=selected_values, plus_list=options)
            options_to_save = get_list_calculated(origin_list=options_to_save, dedup=True)
            set_values_to_historical_file(f_historical=f_historical, values=options_to_save)
            logging.debug(f'''len(options_to_save)={len(options_to_save)} {"%%%FOO%%% " if QC_MODE else ""}''')

        return selected_values

    except subprocess.CalledProcessError as e:
        if e.returncode == 130:  # User cancelled (Ctrl+C or ESC)
            logging.info("fzf 선택이 사용자에 의해 취소되었습니다.")
            return []
        logging.error(f"fzf 실행 중 오류 발생 (코드: {e.returncode}): {e.stderr.decode('utf-8')}")
        return []
    except Exception as e:
        logging.error(f"fzf 다중 선택 처리 중 예상치 못한 오류 발생: {e}")
        return []

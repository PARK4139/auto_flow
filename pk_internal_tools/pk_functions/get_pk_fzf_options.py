from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_etc import PK_POINTER_COLOR, PK_PROMPT_COLOR, PK_HL_COLOR, PK_FG_ACTIVE_COLOR, PK_HL_ACTIVE_COLOR, PK_QUERY_COLOR, PK_POINTER_TEXT, PK_SPINNER_COLOR


@ensure_seconds_measured
def get_pk_fzf_options(prompt_text=None):
    from pk_internal_tools.pk_functions.get_fzf_prompt_text import get_fzf_prompt_text
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    import platform

    if prompt_text is None:
        prompt_text = get_fzf_prompt_text()

    opening_command = 'xdg-open "{}"'  # 기본 파일 열기 명령
    copy_command = "xclip -selection clipboard"  # 기본 클립보드 복사 명령
    fzf_preview_option = 'bat --style=numbers --color=always "{}"'  # 컬러 미리보기 도구

    if is_os_windows():
        opening_command = 'start "" explorer.exe "{}"'  # Windows에서 explorer로 열기
        copy_command = 'clip.exe'  # Windows 클립보드 복사 도구
        fzf_preview_option = 'type "{}"'  # Windows 기본 텍스트 출력 명령

    elif is_os_wsl_linux():
        opening_command = 'explorer.exe "{}"'  # Windows explorer로 열기 (WSL)
        copy_command = 'clip.exe'  # WSL에서도 Windows 클립보드 사용 가능
        fzf_preview_option = 'bat --style=numbers --color=always "{}"'  # 텍스트 컬러 미리보기


    bind_options = [
        # "tab:down",  # 이거 바인딩 되면 multi_select 할 수 없음.
        "shift-tab:up",  # Shift+Tab으로 위 항목 이동
        f"ctrl-o:execute({opening_command})",  # Ctrl+O: 선택된 항목 열기
        f"ctrl-y:execute-silent(echo {{}} | {copy_command})",  # Ctrl+Y: 선택된 항목 클립보드 복사
        "ctrl-p:toggle-preview",  # Ctrl+P: 미리보기 토글
        "ctrl-k:kill-line",  # Ctrl+K: 입력창 커서 이후 삭제
        "alt-a:select-all",
    ]

    return [
        "--no-mouse",
        "--no-multi",  # 다중 선택 비활성화
        f"--prompt={prompt_text}",  # 프롬프트 텍스트
        f"--pointer={PK_POINTER_TEXT}",    
        f"--color=query:{PK_QUERY_COLOR},spinner:{PK_SPINNER_COLOR},prompt:{PK_PROMPT_COLOR},pointer:{PK_POINTER_COLOR},hl:{PK_HL_COLOR},hl+:{PK_HL_ACTIVE_COLOR},fg+:{PK_FG_ACTIVE_COLOR}",
        # "--no-info", # [1/100] 같은 정보, multi_select 개수정보 제거
        "--no-preview",
        # "--header", "list",
        # "--preview", fzf_preview_option,  # 미리보기 명령 설정
        # "--preview-window", "down:30%",  # 미리보기 창 아래쪽에 30% 크기로 설정
        # "--footer", "TIP : CTRL+O: 경로열기 | CTRL+X: 파일 열기 | ENTER: 선택",
        # "--clear",  # 종료 시 터미널 클리어
        "--no-border",  # 테두리 없음
        "--no-margin",  # 외곽 여백 제거
        "--no-padding",  # 내부 여백 제거
        # "--height=10",  # fzf 창 높이 제한 (라인 수)
        "--height=20",  # fzf 창 높이 제한 (라인 수)
        # "--sync",  # 동기화 모드로 렌더링 정확도 향상?
        "--no-select-1",  # 항목이 1개여도 자동 선택하지 않음
        "--reverse",  # 최신 항목 위에 표시 (위에서 아래로)
        # "--cycle",  # 리스트 끝 → 처음으로 순환
        "--no-cycle",  # 리스트 끝 → 처음으로 순환하지 않음
        "--no-sort",  # 정렬 비활성화 (렌더링 빠르게)
        "--bind", ",".join(bind_options),  # 바인딩 키 설정
    ]
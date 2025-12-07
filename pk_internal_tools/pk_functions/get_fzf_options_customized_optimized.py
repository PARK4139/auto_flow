from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_fzf_options_customized_optimized(prompt_text=None):
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
        "tab:down",  # Tab으로 아래 항목 이동
        "shift-tab:up",  # Shift+Tab으로 위 항목 이동
        f"ctrl-o:execute({opening_command})",  # Ctrl+O: 선택된 항목 열기
        f"ctrl-y:execute-silent(echo {{}} | {copy_command})",  # Ctrl+Y: 선택된 항목 클립보드 복사
        "ctrl-p:toggle-preview",  # Ctrl+P: 미리보기 토글
        "ctrl-k:kill-line",  # Ctrl+K: 입력창 커서 이후 삭제
    ]

    return [
        "--no-mouse",
        "--no-multi",  # 다중 선택 비활성화
        f"--prompt={prompt_text}",  # 프롬프트 텍스트
        "--pointer=▶",  # 선택 커서 모양
        # "--color=prompt:#ffffff,pointer:#ffffff,hl:#ff6b6b,hl+:#ff6b6b,fg+:#ff6b6b",  # 색상 : 레드
        "--color=prompt:#ffffff,pointer:#4da6ff,hl:#3399ff,hl+:#3399ff,fg+:#3399ff",    # 색상 : 스카이블루
        # "--color=prompt:#ffffff,pointer:#00ced1,hl:#20b2aa,hl+:#20b2aa,fg+:#20b2aa",    # 색상 : 민트블루
        # "--color=prompt:#ffffff,pointer:#4b0082,hl:#483d8b,hl+:#483d8b,fg+:#483d8b",    # 색상 : 다크퍼플
        # "--color=prompt:#ffffff,pointer:#87cefa,hl:#1e90ff,hl+:#1e90ff,fg+:#1e90ff",    # 색상 : 파스텔블루
        "--no-info",                                      # [1/100] 같은 정보 라인 제거
        "--no-preview",
        # "--header", "list",
        # "--preview", fzf_preview_option,  # 미리보기 명령 설정
        # "--preview-window", "down:30%",  # 미리보기 창 아래쪽에 30% 크기로 설정
        # "--footer", "TIP : CTRL+O: 경로열기 | CTRL+X: 파일 열기 | ENTER: 선택",
        # "--clear",  # 종료 시 터미널 클리어
        "--no-border",  # 테두리 없음
        "--no-margin",  # 외곽 여백 제거
        "--no-padding",  # 내부 여백 제거
        "--height=10",  # fzf 창 높이 제한 (라인 수)
        # "--sync",  # 동기화 모드로 렌더링 정확도 향상?
        "--no-select-1",  # 항목이 1개여도 자동 선택하지 않음
        "--reverse",  # 최신 항목 위에 표시 (위에서 아래로)
        "--cycle",  # 리스트 끝 → 처음으로 순환
        "--no-sort",  # 정렬 비활성화 (렌더링 빠르게)
        "--bind", ",".join(bind_options),  # 바인딩 키 설정
    ]



#
#
# @ensure_seconds_measured
# def get_fzf_options_customized_optimized(prompt_text):
#     from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
#     from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
#     opening_command = None
#     copy_command = None
#     fzf_preview_option = None
#     if is_os_windows():
#         opening_command = 'start "" explorer.exe'
#         copy_command = 'clip.exe'
#         # fzf_preview_option = 'type'
#         # fzf_preview_option = 'bat --style=numbers --color=always'  # bat는 cat보다 보기 좋은 컬러 출력 툴, Windows에서도 scoop install bat이나 choco install bat으로 설치 가능
#         # fzf_preview_option = 'code'  # bat는 cat보다 보기 좋은 컬러 출력 툴, Windows에서도 scoop install bat이나 choco install bat으로 설치 가능
#         fzf_preview_option = "'ueberzug layer --parser json --action add --identifier preview --x 0 --y 0 --path {}" # 썸네일 출력, ueberzug 의존
#     elif is_os_wsl_linux():
#         opening_command = 'explorer.exe "{}"'
#         copy_command = 'clip.exe'
#         # fzf_preview_option = 'cat'
#         fzf_preview_option = 'bat --style=numbers --color=always'
#     else:
#         opening_command = 'xdg-open'
#         copy_command = 'TODO'
#         fzf_preview_option = 'cat'
#
#     bind_actions = [
#         "tab:down",
#         "shift-tab:up",
#         f"ctrl-o:execute({opening_command} {{}})",  # {} == 선택된 항목
#         # "ctrl-x:execute(open {})",
#         "ctrl-p:toggle-preview",                               # fzf preview toggle
#         # "ctrl-u"                                             # fzf 입력란 기준 앞줄 삭제
#         "ctrl-k:kill-line",                                    # fzf 입력란 기준 뒷줄 삭제
#         # alt f                                                # fzf 입력란 _ 기준 앞단어로 이동
#         # alt b                                                # fzf 입력란 _ 기준 뒷단어로 이동
#         # ctrl c                                               # fzf 종료
#         # ctrl w                                               # fzf 입력란 word 삭제
#         f"ctrl-y:execute-silent(echo {{}} | {copy_command})",  # save selected to clipboard
#         # "Ctrl-F:execute-silent(추가바인딩가능)",
#         # "alt-숫자:execute-silent(추가바인딩가능)",
#         # "alt-문자:execute-silent(추가바인딩가능)",
#     ]
#     return [
#         # "--no-mouse",
#         "--no-multi",  # 다중 선택 비활성화
#         f"--prompt={prompt_text}",
#         "--pointer=▶",
#         "--color=prompt:#ffffff,pointer:#ffffff,hl:#ff6b6b,hl+:#ff6b6b,fg+:#ff6b6b",
#         "--no-info",  # 정보 라인 제거 # [/파일개수] 정보
#         # "--no-preview",
#         "--preview", f"{fzf_preview_option} {{}}",
#         # "--preview-window", "right:40%",
#         "--preview-window", "down:30%",
#         "--clear",  # 화면 클리어 비활성화
#         "--no-border",  # 테두리 제거
#         "--no-margin",  # 여백 제거
#         "--no-padding",  # 패딩 제거
#         "--height=10",  # 고정 높이로 메모리 최적화
#         "--sync",
#         # "--exit-0",  # 항목 없으면 종료 (Windows에서 문제 발생)
#         "--no-select-1",  # 자동 선택 비활성화 (Enter 필요)
#         # "--select-1",  # 항목이 1개면 자동 선택 (Enter 필요하므로 제거)
#         #  추가 속도 최적화
#         "--reverse",  # 역순 표시
#         "--cycle",  # 순환 선택으로 빠른 네비게이션
#         "--bind", ",".join(bind_actions),  # 빠른 키바인딩
#
#         # 렌더링 속도 최적화 기대옵션
#         # "--ansi",  # ANSI 색상으로 빠른 렌더링
#         # "--tac",  # 역순으로 최근 항목 우선
#         # "--border=none",  # 테두리 제거로 렌더링 최적화
#         # "--margin=0",  # 여백 제거
#         # "--padding=0",  # 패딩 제거
#         "--no-sort",  # 렌더링 속도 최적화 기대옵션
#     ]

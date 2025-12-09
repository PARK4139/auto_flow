"""
Windows doskey 등록 함수

fzf를 사용하여 등록할 doskey를 선택하고 등록하는 함수
Library로 사용할 때 setup.cmd 없이 doskey만 등록할 수 있습니다.
"""
from af_internal_tools.constants.af_file_paths import F_AUTO_FLOW_터미널_실행_PY
from pk_internal_tools.pk_functions.ensure_pk_autorun_registered import ensure_pk_autorun_registered
from pk_internal_tools.pk_functions.ensure_pk_doskey_bat_created_with_selected_doskeys import ensure_pk_doskey_bat_created_with_selected_doskeys
from pk_internal_tools.pk_functions.ensure_values_completed_2025_11_23 import ensure_values_completed_2025_11_23
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import (
    D_DOWNLOADS,
    D_PK_MEMO_REPO,
    D_PK_WORKING,
    D_BUSINESS_FLOW_REPO,
    d_pk_external_tools,
    D_DESKTOP,
    D_PK_RECYCLE_BIN, d_pk_root,
)
from pk_internal_tools.pk_objects.pk_files import (
    F_PK_ENSURE_PK_COMMANDER_EXECUTED_PY,
    F_UV_EXE,
    F_UV_ACTIVATE_BAT,
    F_VSCODE_LNK,
    F_CLAUDE_LNK,
    f_pycharm64_exe,
    F_ENSURE_CMD_EXE_RAN_AS_ADMIN,
)
from pk_internal_tools.pk_objects.pk_files import F_VENV_PYTHON_EXE, F_PK_ENSURE_PK_WRAPPER_STARTED_PY


def _get_auto_fllow_doskey_commands() -> dict[str, str]:
    """
    등록 가능한 doskey 명령어 딕셔너리를 반환합니다.
    
    Returns:
        dict: {display_name: doskey_command} 형태의 딕셔너리
    """
    uv_exe_path = F_UV_EXE

    doskey_commands = {
        # 디렉토리 이동
        f'1: cd "{D_DOWNLOADS}"': f'doskey 1=cd "{D_DOWNLOADS}"',
        f'2: cd "{d_pk_root}"': f'doskey 2=cd "{d_pk_root}"',
        f'3: cd "{D_PK_MEMO_REPO}"': f'doskey 3=cd "{D_PK_MEMO_REPO}"',
        f'4: cd "{D_PK_WORKING}"': f'doskey 4=cd "{D_PK_WORKING}"',
        f'5: cd "{D_BUSINESS_FLOW_REPO}"': f'doskey 5=cd "{D_BUSINESS_FLOW_REPO}"',
        f'6: cd "{d_pk_external_tools}"': f'doskey 6=cd "{d_pk_external_tools}"',
        f'7: cd "{d_pk_external_tools}"': f'doskey 7=cd "{d_pk_external_tools}"',
        f'9: cd "{D_DESKTOP}"': f'doskey 9=cd "{D_DESKTOP}"',
        f'0: cd "{D_PK_RECYCLE_BIN}"': f'doskey 0=cd "{D_PK_RECYCLE_BIN}"',

        # PK System 명령어
        # 프로젝트 루트로 이동 후 .venv Python을 사용하여 실행
        # uv run 대신 직접 .venv Python 사용하여 더 안정적
        # f'pk: PK wrapper 시작': f'{f_ensure_pk_wrapper_executed_cmd}',
        f'pk: PK wrapper 실행': f'doskey pk="{F_VENV_PYTHON_EXE}" "{F_PK_ENSURE_PK_WRAPPER_STARTED_PY}"',
        f'pkt: PK Commander 실행': f'doskey pkt="{F_VENV_PYTHON_EXE}" "{F_PK_ENSURE_PK_COMMANDER_EXECUTED_PY}"',
        f'aft: PK Commander 실행': f'doskey pkt="{F_VENV_PYTHON_EXE}" "{F_AUTO_FLOW_터미널_실행_PY}"',

        # 개발 환경
        f'venv: Virtual Environment 활성화': f'doskey venv="{F_UV_ACTIVATE_BAT}"',
        f'vscode: Visual Studio Code 실행': f'doskey vscode="{F_VSCODE_LNK}" $*',
        f'claude: Claude 실행': f'doskey claude="{F_CLAUDE_LNK}" $*',
        f'pycharm: PyCharm 실행': f'doskey pycharm=start "" "{f_pycharm64_exe}" $*',

        # os terminal
        f'ps: PowerShell 실행': f'doskey ps=powershell',
        f'psa: PowerShell (관리자) 실행': f'doskey psa=powershell -Command "Start-Process powershell -Verb RunAs"',
        f'cmda: CMD (관리자) 실행': f'doskey cmda=start "" "{F_ENSURE_CMD_EXE_RAN_AS_ADMIN}"',
        f'x: 종료': f'doskey x=exit',

        # os control
        f'reboot: 시스템 재시작': f'doskey reboot=shutdown /r /t 0',
        f'poweroff: 시스템 종료': f'doskey poweroff=shutdown /s /t 0',
        f'logout: 로그아웃': f'doskey logout=logoff',

        # 유틸리티
        f'.: 탐색기로 현재 디렉토리 열기': f'doskey .=explorer.exe .',
        f'ls: 디렉토리 목록 (간단)': f'doskey ls=dir /b',
        f'cat: 파일 내용 출력': f'doskey cat=type $*',
        f'which: 실행 파일 경로 찾기': f'doskey which=where $*',
        f'pwd: 현재 디렉토리': f'doskey pwd=cd $*',
        f'history: doskey 히스토리': f'doskey history=doskey /history',
        f'play: 파일실행(영상)': f'doskey play=explorer.exe $*',
        f'open: 파일실행(문서)': f'doskey open=explorer.exe $*',

        # WSL
        f'wsld: WSL Ubuntu 실행': f'doskey wsld=wsl --distribution Ubuntu',
        f'wsl24: WSL Ubuntu-24.04 실행': f'doskey wsl24=wsl --distribution Ubuntu-24.04',
        f'wsl20: WSL Ubuntu-20.04 실행': f'doskey wsl20=wsl --distribution Ubuntu-20.04',
        f'wsl18: WSL Ubuntu-18.04 실행': f'doskey wsl18=wsl --distribution Ubuntu-18.04',
    }

    return doskey_commands


def ensure_pk_doskey_registered():
    """
    fzf를 사용하여 doskey를 멀티 선택하고 autorun으로 등록합니다.
    
    doskey 명령어를 fzf에 표시하고, 사용자가 선택한 여러 doskey를 pk_doskey.bat 파일에 등록하고
    Windows CMD AutoRun에 등록합니다. 새 CMD 창이 열릴 때마다 선택된 doskey들이 자동으로 등록됩니다.
    """
    try:
        import logging

        # doskey 명령어 딕셔너리 가져오기
        pk_doskey_commands = _get_auto_fllow_doskey_commands()

        # fzf 옵션 목록 생성 (표시 이름)
        doskey_options = list(pk_doskey_commands.keys())

        if not doskey_options:
            logging.warning("등록할 doskey가 없습니다.")
            return False

        # fzf로 doskey 멀티 선택
        func_n = get_caller_name()
        selected_doskey_displays = ensure_values_completed_2025_11_23(
            key_name="doskey_to_register",
            options=doskey_options,
            func_n=func_n,
            multi_select=True,
            guide_text="등록할 doskey를 멀티 선택하세요 (Tab으로 선택, Enter로 완료):",
            history_reset=True
        )

        if not selected_doskey_displays:
            logging.warning("선택된 doskey가 없어 등록을 종료합니다.")
            return False

        # 선택된 doskey들의 실제 명령어 가져오기
        selected_doskey_command_list = []
        for selected_display in selected_doskey_displays:
            if selected_display not in pk_doskey_commands:
                logging.warning(f"선택된 doskey '{selected_display}'에 대한 명령어를 찾을 수 없습니다. 건너뜁니다.")
                continue
            doskey_command = pk_doskey_commands[selected_display]
            # 'doskey ' 부분 제거 (bat 파일에서 다시 추가)
            if doskey_command.startswith('doskey '):
                selected_doskey_command_list.append(doskey_command)
            else:
                selected_doskey_command_list.append(f'doskey {doskey_command}')

        if not selected_doskey_command_list:
            logging.error("유효한 doskey 명령어가 없습니다.")
            return False

        # bat 파일 생성
        logging.info(f"선택된 {len(selected_doskey_command_list)}개의 doskey로 bat 파일 생성 중...")
        try:
            bat_file = ensure_pk_doskey_bat_created_with_selected_doskeys(selected_doskey_command_list)
            logging.info(f"bat 파일 생성 완료: {bat_file}")
        except Exception as e:
            logging.error(f"bat 파일 생성 실패: {e}")
            import traceback
            logging.debug(traceback.format_exc())
            return False

        # autorun 등록
        logging.info("AutoRun 등록 중...")
        try:
            ensure_pk_autorun_registered()
            logging.info("✅ AutoRun 등록 완료")
        except Exception as e:
            logging.error(f"AutoRun 등록 실패: {e}")
            import traceback
            logging.debug(traceback.format_exc())
            return False

        logging.info(f"doskey 등록 완료! 선택된 {len(selected_doskey_command_list)}개의 doskey가 새 CMD 창에서 자동으로 등록됩니다.")
        return True

    except Exception as e:
        logging.error(f"doskey 등록 중 오류 발생: {e}")
        import traceback
        logging.debug(traceback.format_exc())
        return False

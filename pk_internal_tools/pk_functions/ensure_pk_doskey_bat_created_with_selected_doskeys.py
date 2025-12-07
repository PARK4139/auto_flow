import logging
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_files import F_PK_DOSKEY_BAT, F_UV_EXE


@ensure_seconds_measured
def ensure_pk_doskey_bat_created_with_selected_doskeys(selected_doskey_commands: list[str], uv_exe_path: str = None) -> Path:
    """
    선택된 doskey 명령어 목록을 받아서 pk_doskey.bat 파일을 생성합니다.

    Args:
        selected_doskey_commands: 등록할 doskey 명령어 목록 (예: ['doskey pk=...', 'doskey pkc=...'])
        uv_exe_path: uv.exe 경로 (None이면 F_UV_EXE 사용)

    Returns:
        Path: 생성된 bat 파일 경로
    """
    try:
        import textwrap
        f_ensure_pk_doskey_enabled_bat = F_PK_DOSKEY_BAT

        if uv_exe_path is None:
            uv_exe_path = F_UV_EXE

        # bat 파일 내용 생성
        batch_content = textwrap.dedent(f'''
            @echo off
            chcp 65001 >NUL
        ''').lstrip()

        # 선택된 doskey 명령어들 추가
        for doskey_command in selected_doskey_commands:
            batch_content += f"\n    {doskey_command}"

        batch_content += "\n"

        # 디렉토리 생성 및 파일 쓰기
        f_ensure_pk_doskey_enabled_bat.parent.mkdir(parents=True, exist_ok=True)
        with open(f_ensure_pk_doskey_enabled_bat, 'w', encoding='utf-8') as f:
            f.write(batch_content)

        if f_ensure_pk_doskey_enabled_bat.exists():
            logging.debug(f'''{f_ensure_pk_doskey_enabled_bat} 생성완료 ''')
            return f_ensure_pk_doskey_enabled_bat
        else:
            logging.debug(f'''{f_ensure_pk_doskey_enabled_bat} 생성실패 ''')
            raise FileNotFoundError(f"bat 파일 생성 실패: {f_ensure_pk_doskey_enabled_bat}")
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass

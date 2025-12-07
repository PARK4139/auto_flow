import logging


from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_directories import d_pk_root


def build_pk_project_via_pyinstaller():
    import os

    # 프로젝트 d로 이동
    os.chdir(d_pk_root)

    if is_pnx_existing(pnx=D_VENV):
        logging.debug(f"{D_VENV} d가 있습니다")

        # 현재d의 불필요한 타겟들을 삭제
        items_useless = [
            rf"{d_pk_root}\pk.exe",
            rf"{d_pk_root}\build",
            rf"{d_pk_root}\dist",
            rf"{d_pk_root}\_internal",
            rf"{d_pk_root}\dist.zip",
            rf"{d_pk_root}\pk.spec",
        ]
        for item in items_useless:
            reensure_pnx_moved_parmanently(pnx=item)

        # pip 업그레이드
        ensure_command_executed(cmd="python -m pip install --upgrade pip")

        # pip 업그레이드
        ensure_command_executed(cmd="pip install pyinstaller --upgrade")

        if not QC_MODE:
            ensure_command_executed(cmd=rf"python -m PyInstaller -i .\pk_external_tools\icon.PNG pk_test_test.py")

        if QC_MODE:
            ensure_command_executed(cmd=rf'echo d | xcopy ".\pk_external_tools" ".\dist\pk_test_test\_internal\pk_external_tools" /e /h /k /y')

        # f = f'{d_pk_system}/pk_temp.py'
        # write_f(f)

        # virtual environment 을 활성화하고, 그 후에 파이썬 스크립트 exec
        # run

        # pk_temp.py
        # os.remove(f)

    else:
        logging.debug(f"{D_VENV} d가 없습니다")

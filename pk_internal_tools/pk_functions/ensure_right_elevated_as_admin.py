from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE


@ensure_seconds_measured
def ensure_right_elevated_as_admin():
    # ---------------- UAC 승격 래퍼 ----------------
    import os, sys, ctypes, subprocess

    def is_admin() -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def elevate_and_rerun():

        py = F_UV_PYTHON_EXE if os.path.exists(F_UV_PYTHON_EXE) else sys.executable
        script = os.path.abspath(__file__)
        params = f'"{script}" --elevated'
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", py, params, None, 1)
            sys.exit(0)
        except Exception:
            ps = (
                'powershell -NoProfile -Command '
                f'"Start-Process \'{py}\' \'{script} --elevated\' -Verb RunAs"'
            )
            subprocess.call(ps, shell=True)
            sys.exit(0)

    if not is_admin() and "--elevated" not in sys.argv:
        elevate_and_rerun()

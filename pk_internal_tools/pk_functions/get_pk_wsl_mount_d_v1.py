
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging
from pathlib import Path

def get_pk_wsl_mount_d_v1(windows_path, path_to_mount):
    if is_os_wsl_linux():
        check_root_right()
        import subprocess
        import os
        import sys
        # n. 사용자 입력 받기
        ensure_pnx_made(pnx=windows_path, mode='f')
        windows_path = windows_path
        mount_point = path_to_mount
        windows_path = get_pnx_windows_style(pnx=windows_path)

        try:
            # 3) 마운트 지점 디렉토리 생성
            print(f"[*] 디렉토리 생성: sudo mkdir -p {mount_point}")
            subprocess.run(["sudo", "mkdir", "-p", mount_point], check=True)

            # 4) drvfs 마운트
            print(f"[*] 마운트: sudo mount -t drvfs '{windows_path}' {mount_point}")
            subprocess.run(["sudo", "mount", "-t", "drvfs", windows_path, mount_point], check=True)

            # current session
            # sudo mkdir -p /home/pk/Downloads/pk_working
            # sudo mount -t drvfs 'C:\Users\WIN10PROPC3\Downloads\pk_working' /home/pk/Downloads/pk_working
            # sudo chown 1000:1000 /home/pk/Downloads/pk_working

            # 5) 소유권을 현재 WSL 사용자로 변경
            uid = os.getuid()
            gid = os.getgid()
            print(f"[*] 소유권 변경: sudo chown {uid}:{gid} {mount_point}")
            subprocess.run(["sudo", "chown", f"{uid}:{gid}", mount_point], check=True)

        except subprocess.CalledProcessError as e:
            print(f"\n[!] 오류 발생 (exit {e.returncode}):\n{e.stdout or e.output}")
            sys.exit(1)

        if Path(mount_point).exists():
            print(f"{mount_point} is mounted successfully.")
    elif is_os_windows():
        logging.debug(f'''get_pk_wsl_mount_d is not supported in Windows. ''')
    else:
        # (순수 Linux 등, WSL도 아니고 Windows도 아닌 경우 별도 처리 없음)
        pass

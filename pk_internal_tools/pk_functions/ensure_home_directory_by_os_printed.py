import os
import subprocess

def get_USERPROFILE_cmd_style():
    return os.environ.get("USERPROFILE", "")

def get_USERPROFILE_linux_style():
    return os.environ.get("HOME", "")

def get_USERPROFILE_wsl_style():
    USERPROFILE_cmd_style = get_USERPROFILE_cmd_style()
    if USERPROFILE_cmd_style:
        USERPROFILE_cmd_style = USERPROFILE_cmd_style.replace("\\", "/")  # 경로 구분자 변환
    if USERPROFILE_cmd_style.startswith("C:/"):
        return "/mnt/c" + USERPROFILE_cmd_style[2:]

def check_wsl():
    """현재 환경이 WSL인지 확인"""
    try:
        # WSL 환경에서는 /proc/version 파일에 "microsoft"가 포함됨
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                return True
    except FileNotFoundError:
        pass
    return False

def check_linux():
    """현재 환경이 Linux인지 확인"""
    return os.name == "posix" and os.uname().sysname.lower() == "linux"


def ensure_home_directory_by_os_printed():
    # 환경 변수를 Python 딕셔너리로 변환
    env_vars = subprocess.check_output(["cmd.exe", "/C", "set"], text=True)
    for line in env_vars.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ[key] = value

    # 환경 체크
    if check_wsl():
        USERPROFILE_wsl_style = get_USERPROFILE_wsl_style()
        print(USERPROFILE_wsl_style)
    elif check_linux():
        USERPROFILE_linux_style = get_USERPROFILE_linux_style()
        print(USERPROFILE_linux_style)
    else:
        USERPROFILE_cmd_style = get_USERPROFILE_cmd_style()
        print(USERPROFILE_cmd_style)




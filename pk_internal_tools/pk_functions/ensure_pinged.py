from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
import logging
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_etc import PK_BLANK
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_pinged(ip):
    return ensure_pinged_2025_11_22(ip)


def ensure_pinged_2024_03(ip):
    # pk : windows 10 pro 에서 정상동작 확인
    # pk : 다만 평균속도가 1초로 느린편

    if not ip:
        logging.debug(f'''ping {ip} ''')
        return 0
    signature = None
    if is_os_windows():
        cmd = rf"ping -n 1 -w 500 {ip}"  # 3600000ms 타임아웃
        signature_list = ["(0% loss)", '(0% 손실)']
    else:
        cmd = rf"ping -c 1 -W 0.5 {ip}"  # 3600초 타임아웃
        signature_list = [f'{PK_BLANK}0% packet loss']
    std_list = ensure_command_executed(cmd=cmd, encoding=PkEncoding.UTF8)
    for line in std_list:
        if any(signature in line for signature in signature_list):
            if QC_MODE:
                logging.debug(f'''ping {ip} ''')
            return 1
    logging.debug(f'''ping {ip} ''')
    return 0


def ensure_pinged_2024_05(ip, timeout_ms=1000):
    # lazy import
    import subprocess

    if not ip:
        logging.debug(f'ping {ip}')
        return 0

    # OS별 ping 명령어 및 성공 시그널 정의
    if is_os_windows():
        cmd = f"ping -n 1 -w {timeout_ms} {ip}"
        signatures = ["(0% loss)", "(0% 손실)"]
    else:
        sec = max(1, timeout_ms // 1000)
        cmd = f"ping -c 1 -W {sec} {ip}"
        signatures = [f"{PK_BLANK}0% packet loss"]

    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,  # universal_newlines=True 와 동일
            encoding='utf-8',  # utf-8로 디코딩 시도
            errors='ignore'  # 디코딩 오류 무시
        )
        stdout, _ = proc.communicate(timeout=(timeout_ms / 1000) + 0.5)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout = ""
    except Exception:
        stdout = ""

    # None 또는 빈값 방어
    if not stdout:
        stdout = ""

    # 결과 판정
    for line in stdout.splitlines():
        if any(sig in line for sig in signatures):
            if QC_MODE:
                logging.debug(f'ping {ip}')
            return 1

    logging.debug(f'ping {ip}')
    return 0


def ensure_pinged_2025_11_22(ip, timeout_ms=1000):
    import subprocess
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_etc import PK_BLANK

    if not ip:
        logging.debug(f'ping {ip}')
        return 0

    # OS별 명령어 및 성공 시그널 정의
    if is_os_windows():
        cmd = f"ping -n 1 -w {timeout_ms} {ip}"
        signatures = ["(0% loss)", "(0% 손실)"]
        encoding = 'mbcs'  # ANSI 코드 페이지(한국어 Windows: CP949)
    else:
        sec = max(1, timeout_ms // 1000)
        cmd = f"ping -c 1 -W {sec} {ip}"
        signatures = [f"{PK_BLANK}0% packet loss"]
        encoding = 'utf-8'

    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding=encoding,
            errors='ignore'
        )
        stdout, _ = proc.communicate(timeout=(timeout_ms / 1000) + 0.5)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout = ""
    except Exception:
        stdout = ""

    # stdout이 None이거나 빈값 방어
    if not stdout:
        stdout = ""

    # **리턴코드 우선 검사** (0이면 성공)
    if proc.returncode == 0:
        if QC_MODE:
            logging.debug(f'ping {ip}')
        return 1

    # 리턴코드로도 판단 안 될 때만 시그니처 검사
    for line in stdout.splitlines():
        if any(sig in line for sig in signatures):
            if QC_MODE:
                logging.debug(f'ping {ip}')
            return 1

    logging.debug(f'ping {ip}')
    return 0

#!/usr/bin/env python3

"""
관리자 권한 확인 및 자동 상승 처리 모듈
- Windows 환경에서 관리자 권한이 필요한 작업을 위한 유틸리티
- 권한 확인, 자동 상승, UAC 처리 등을 담당
"""

import os
import sys
import logging
import subprocess
from typing import Optional, Tuple, List
from pathlib import Path


def is_admin() -> bool:
    """
    현재 프로세스가 관리자 권한으로 실행 중인지 확인
    
    Returns:
        bool: 관리자 권한이면 True, 아니면 False
    """
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception as e:
        # fallback: 'net session'은 관리자만 성공
        try:
            result = subprocess.run(
                ["net", "session"], 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='ignore'
            )
            return result.returncode == 0
        except Exception as e:
            return False


def request_admin_privilege(script_path: Optional[str] = None, args: Optional[List[str]] = None) -> bool:
    """
    관리자 권한으로 현재 스크립트를 재실행 요청 (ShellExecuteExW 사용)

    Args:
        script_path: 실행할 스크립트 경로 (None이면 현재 스크립트)
        args: 추가 인자들

    Returns:
        bool: 권한 상승 요청 성공 여부
    """
    if is_admin():
        logging.debug("이미 관리자 권한으로 실행 중입니다.")
        return True

    try:
        import ctypes
        # win32api, win32con, win32process는 ShellExecuteExW를 직접 호출할 때 필요할 수 있으나,
        # ctypes만으로 ShellExecuteExW를 호출하는 것이 일반적입니다.
        # win32api.GetLastError()를 사용하기 위해 win32api는 필요합니다.
        import win32api
        import win32con # SW_SHOWNORMAL

        # 실행할 스크립트 경로 결정
        if script_path is None:
            script_path = sys.argv[0]

        # 인자 준비
        if args is None:
            args = sys.argv[1:]
        
        # 인자를 하나의 문자열로 결합
        # ShellExecuteExW의 lpParameters는 단일 문자열을 기대합니다.
        # 스크립트 경로와 인자들을 공백으로 구분하여 결합합니다.
        # 인자에 공백이 포함될 경우를 대비하여 큰따옴표로 묶습니다.
        arg_str = " ".join([f'"{arg}"' if " " in arg else arg for arg in args])

        logging.info("🔐 관리자 권한 상승을 요청합니다...")
        logging.info("💡 UAC 창이 나타나면 '예'를 클릭하세요.")

        # Python 인터프리터 경로를 직접 지정
        python_exe = sys.executable

        # SHELLEXECUTEINFO 구조체 정의
        class SHELLEXECUTEINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("fMask", ctypes.c_ulong),
                ("hwnd", ctypes.c_ulong),
                ("lpVerb", ctypes.c_wchar_p),
                ("lpFile", ctypes.c_wchar_p),
                ("lpParameters", ctypes.c_wchar_p),
                ("lpDirectory", ctypes.c_wchar_p),
                ("nShow", ctypes.c_ulong),
                ("hInstApp", ctypes.c_void_p),
                ("lpIDList", ctypes.c_void_p),
                ("lpClass", ctypes.c_wchar_p),
                ("hkeyClass", ctypes.c_void_p),
                ("dwHotKey", ctypes.c_ulong),
                ("hIcon", ctypes.c_void_p),
                ("hProcess", ctypes.c_void_p), # 출력 필드
            ]

        SEE_MASK_NOCLOSEPROCESS = 0x00000040 # 프로세스 핸들을 얻기 위함
        SW_SHOWNORMAL = 1 # 정상적인 창으로 표시

        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(sei)
        sei.fMask = SEE_MASK_NOCLOSEPROCESS
        sei.hwnd = 0 # 부모 윈도우 없음
        sei.lpVerb = "runas" # 관리자 권한으로 실행
        sei.lpFile = python_exe # 실행할 프로그램 (python.exe)
        # lpParameters는 실행할 스크립트 경로와 그 스크립트의 인자들을 포함
        sei.lpParameters = f'"{script_path}" {arg_str}'
        sei.lpDirectory = os.getcwd() # 현재 작업 디렉토리
        sei.nShow = SW_SHOWNORMAL

        # ShellExecuteExW 호출
        if ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
            # 성공적으로 새 프로세스 시작 요청
            # 새 프로세스가 시작될 때까지 기다릴 필요는 없음 (원래 프로세스는 종료될 것이므로)
            logging.info("관리자 권한으로 재실행 요청 성공")
            return True
        else:
            # 실패 (예: 사용자 취소, 오류)
            error_code = win32api.GetLastError() # 마지막 오류 코드 가져오기
            logging.warning(f"관리자 권한 상승 실패 또는 사용자 취소 (오류 코드: {error_code})")
            return False

    except Exception as e:
        logging.error(f"관리자 권한 상승 중 오류: {e}")
        return False



def ensure_admin_privilege_or_exit(auto_elevate: bool = True) -> bool:
    """
    관리자 권한 확인 및 필요시 자동 상승 또는 종료
    
    Args:
        auto_elevate: True이면 자동으로 권한 상승 시도, False이면 오류 발생
        
    Returns:
        bool: 관리자 권한 확보 성공 여부
        
    Raises:
        RuntimeError: 관리자 권한이 없고 auto_elevate=False인 경우
    """
    if is_admin():
        logging.debug("✅ 관리자 권한 확인됨")
        return True
    
    if auto_elevate:
        logging.warning("⚠️ 관리자 권한이 필요합니다. 자동 상승을 시도합니다...")
        success = request_admin_privilege()
        if success:
            # 권한 상승 성공 시 현재 프로세스 종료 (새 프로세스가 실행됨)
            sys.exit(0)
        else:
            logging.error("❌ 관리자 권한 상승 실패")
            return False
    else:
        # 자동 상승하지 않고 오류 발생
        current_script = Path(sys.argv[0]).name
        raise RuntimeError(
            f"관리자 권한이 필요합니다. 현재 권한으로는 WLAN 서비스/인터페이스 제어가 거부됩니다.\n"
            f"관리자 PowerShell에서 다음 중 하나로 실행하세요:\n"
            f"  1) python {sys.argv[0]}\n"
            f"  2) 또는 스크립트를 마우스 오른쪽 → '관리자 권한으로 실행'\n"
        )


def get_admin_status_info() -> dict:
    """
    현재 관리자 권한 상태 정보 반환
    
    Returns:
        dict: 권한 상태 정보
    """
    admin_status = is_admin()
    
    info = {
        'is_admin': admin_status,
        'current_user': os.environ.get('USERNAME', 'unknown'),
        'process_id': os.getpid(),
        'script_path': sys.argv[0] if sys.argv else 'unknown'
    }
    
    if admin_status:
        info['status_message'] = "✅ 관리자 권한으로 실행 중"
    else:
        info['status_message'] = "⚠️ 일반 사용자 권한으로 실행 중"
    
    return info


def run_as_admin_if_needed(func, *args, **kwargs):
    """
    함수를 관리자 권한으로 실행 (필요시 권한 상승)
    
    Args:
        func: 실행할 함수
        *args: 함수 인자
        **kwargs: 함수 키워드 인자
        
    Returns:
        함수 실행 결과 또는 권한 상승 후 종료
    """
    if not is_admin():
        logging.warning("⚠️ 관리자 권한이 필요한 함수입니다. 권한 상승을 시도합니다...")
        success = request_admin_privilege()
        if success:
            sys.exit(0)  # 새 프로세스에서 실행됨
        else:
            raise RuntimeError("관리자 권한 상승에 실패했습니다.")
    
    # 관리자 권한으로 함수 실행
    logging.debug("✅ 관리자 권한으로 함수 실행")
    return func(*args, **kwargs)


if __name__ == "__main__":
    # 테스트 코드
    # 
    
    logging.debug("관리자 권한 모듈 테스트")
    
    # 현재 권한 상태 확인
    status = get_admin_status_info()
    for key, value in status.items():
        logging.debug(f"{key}: {value}")
    
    # 관리자 권한 확인
    if is_admin():
        logging.debug("✅ 관리자 권한으로 실행 중입니다.")
    else:
        logging.debug("⚠️ 일반 사용자 권한으로 실행 중입니다.")
        logging.debug("💡 관리자 권한이 필요한 작업은 자동으로 권한 상승을 시도합니다.")

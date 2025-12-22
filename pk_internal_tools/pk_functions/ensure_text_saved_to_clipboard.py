import logging


def ensure_text_saved_to_clipboard(text):
    """
    클립보드에 텍스트를 복사하는 함수
    - WSL 환경에서는 PowerShell Set-Clipboard 사용
    - Windows 환경에서는 clipboard 라이브러리 사용
    - Linux 환경에서는 xclip 또는 xsel 사용
    """
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
    
    if is_os_wsl_linux():
        # WSL 환경에서는 PowerShell Set-Clipboard 사용
        try:
            import subprocess
            # PowerShell 명령어로 클립보드에 복사
            cmd = f'Set-Clipboard -Value "{text}"'
            subprocess.run(['powershell.exe', '-Command', cmd], check=True)
            return text
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.debug(f"WSL 클립보드 복사 실패: {str(e)}")
            return text
    elif is_os_windows():
        # Windows에서는 clipboard 라이브러리 사용
        try:
            import clipboard
            clipboard.copy(text)
            return text
        except ImportError:
            logging.debug(f"Windows 클립보드 복사 실패. clipboard 모듈이 없습니다.")
            return text
    elif is_os_linux():
        # Linux에서는 xclip 또는 xsel 사용
        try:
            import subprocess
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
            return text
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['xsel', '--clipboard'], input=text.encode(), check=True)
                return text
            except (subprocess.CalledProcessError, FileNotFoundError):
                # 클립보드 도구가 없으면 출력만
                logging.debug(f"Linux 클립보드 복사 실패. 텍스트: {text}")
                return text
    else:
        # macOS에서는 pbcopy 사용
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=text.encode(), check=True)
            return text
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.debug(f"macOS 클립보드 복사 실패. 텍스트: {text}")
            return text
    
    return text

import platform
import os
import subprocess

def is_os_wsl_linux():
    """
    WSL 환경인지 확인하는 강화된 함수
    Returns:
        bool: WSL 환경이면 True, 아니면 False
    """
    try:
        # 방법 1: platform.uname().release에서 "microsoft" 확인
        try:
            release_info = platform.uname().release.lower()
            if "microsoft" in release_info or "wsl" in release_info:
                return True
        except Exception:
            pass
        
        # 방법 2: /proc/version 파일에서 WSL 관련 문자열 확인
        try:
            if os.path.exists('/proc/version'):
                with open('/proc/version', 'r', encoding='utf-8', errors='ignore') as f:
                    version_content = f.read().lower()
                    if 'microsoft' in version_content or 'wsl' in version_content:
                        return True
        except Exception:
            pass
        
        # 방법 3: 환경변수에서 WSL 관련 정보 확인
        try:
            wsl_env_vars = ['WSL_DISTRO_NAME', 'WSL_INTEROP', 'WSLENV', 'WSL_INTEROP_PIPE']
            for env_var in wsl_env_vars:
                if env_var in os.environ:
                    return True
        except Exception:
            pass
        
        # 방법 4: /proc/sys/kernel/osrelease 파일 확인
        try:
            if os.path.exists('/proc/sys/kernel/osrelease'):
                with open('/proc/sys/kernel/osrelease', 'r', encoding='utf-8', errors='ignore') as f:
                    osrelease_content = f.read().lower()
                    if 'microsoft' in osrelease_content or 'wsl' in osrelease_content:
                        return True
        except Exception:
            pass
        
        # 방법 5: /etc/os-release 파일 확인
        try:
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r', encoding='utf-8', errors='ignore') as f:
                    osrelease_content = f.read().lower()
                    if 'microsoft' in osrelease_content or 'wsl' in osrelease_content:
                        return True
        except Exception:
            pass
        
        # 방법 6: uname 명령어 실행 결과 확인
        try:
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                uname_output = result.stdout.lower()
                if 'microsoft' in uname_output or 'wsl' in uname_output:
                    return True
        except Exception:
            pass
        
        # 방법 7: /mnt/c 경로 존재 및 접근 가능성 확인 (보조적)
        try:
            if os.path.exists('/mnt/c') and os.access('/mnt/c', os.R_OK):
                # Windows 경로가 실제로 접근 가능한지 추가 확인
                if os.path.exists('/mnt/c/Users') and os.access('/mnt/c/Users', os.R_OK):
                    # 추가로 Windows 명령어 실행 가능 여부 확인
                    try:
                        result = subprocess.run(['cmd.exe', '/c', 'echo', 'test'], 
                                             capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            return True
                    except Exception:
                        pass
        except Exception:
            pass
        
        # 방법 8: /proc/self/mounts에서 Windows 파일시스템 확인
        try:
            if os.path.exists('/proc/self/mounts'):
                with open('/proc/self/mounts', 'r', encoding='utf-8', errors='ignore') as f:
                    mounts_content = f.read().lower()
                    if 'drvfs' in mounts_content or '9p' in mounts_content:
                        return True
        except Exception:
            pass
        
        return False
        
    except Exception as e:
        # 에러 발생 시 기본값으로 False 반환
        return False

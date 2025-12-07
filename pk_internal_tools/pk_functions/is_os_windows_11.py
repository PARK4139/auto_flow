"""
Windows 11인지 확인하는 함수
"""
import platform
import subprocess
from typing import Optional


def is_os_windows_11() -> bool:
    """
    Windows 11인지 확인합니다.
    
    여러 방법을 시도하여 정확도를 높입니다:
    1. 레지스트리 확인 (가장 확실)
    2. PowerShell 명령어
    3. platform 모듈 (보조)
    
    Returns:
        bool: Windows 11이면 True, 아니면 False
    """
    # Windows가 아니면 False
    if platform.system() != 'Windows':
        return False
    
    # 방법 1: 레지스트리 확인 (가장 확실)
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )
        
        try:
            # CurrentBuild 또는 CurrentBuildNumber 확인
            # Windows 11은 빌드 번호가 22000 이상
            build_number = winreg.QueryValueEx(key, "CurrentBuild")[0]
            try:
                build_int = int(build_number)
                if build_int >= 22000:  # Windows 11은 22000부터
                    return True
            except (ValueError, TypeError):
                pass
            
            # ReleaseId 확인 (Windows 10은 "2009" 등, Windows 11은 "21H2" 등)
            try:
                release_id = winreg.QueryValueEx(key, "ReleaseId")[0]
                # Windows 11은 ReleaseId가 없거나 다른 형식
                if release_id and release_id.isdigit():
                    # 숫자만 있으면 Windows 10일 가능성 높음
                    if int(release_id) < 2009:
                        return False
            except (FileNotFoundError, ValueError):
                pass
            
            # ProductName 확인
            try:
                product_name = winreg.QueryValueEx(key, "ProductName")[0]
                if "Windows 11" in product_name:
                    return True
            except FileNotFoundError:
                pass
                
        finally:
            winreg.CloseKey(key)
    except Exception:
        pass
    
    # 방법 2: PowerShell 명령어
    try:
        ps_command = """
        $osInfo = Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, WindowsBuildLabEx
        $productName = $osInfo.WindowsProductName
        if ($productName -like "*Windows 11*") {
            Write-Host "Windows11"
            exit 0
        } else {
            exit 1
        }
        """
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=5,
            shell=True
        )
        if result.returncode == 0 and "Windows11" in result.stdout:
            return True
    except Exception:
        pass
    
    # 방법 3: platform 모듈 (보조)
    try:
        version = platform.version()
        # Windows 11은 10.0.22000 이상
        if version:
            parts = version.split('.')
            if len(parts) >= 3:
                try:
                    build = int(parts[2])
                    if build >= 22000:
                        return True
                except (ValueError, IndexError):
                    pass
    except Exception:
        pass
    
    return False


def get_windows_version() -> Optional[str]:
    """
    Windows 버전을 반환합니다.
    
    Returns:
        Optional[str]: "Windows 10", "Windows 11", 또는 None
    """
    if platform.system() != 'Windows':
        return None
    
    if is_os_windows_11():
        return "Windows 11"
    else:
        return "Windows 10"


if __name__ == "__main__":
    # 테스트
    print(f"Windows 11 여부: {is_os_windows_11()}")
    print(f"Windows 버전: {get_windows_version()}")



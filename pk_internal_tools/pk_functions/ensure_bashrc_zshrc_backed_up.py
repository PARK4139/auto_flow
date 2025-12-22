import os
import shutil
import platform
import subprocess
from datetime import datetime


def detect_os():
    """운영체제를 감지하는 함수"""
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    
    os_type = get_os_n()
    
    # WSL 환경인지 추가 확인
    if os_type == "linux":
        if os.path.exists("/proc/version"):
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
                if "microsoft" in version_info or "wsl" in version_info:
                    return "wsl"
        return "linux"
    elif os_type == "windows":
        # Windows에서 WSL이 실행 중인지 확인
        try:
            result = subprocess.run(['wsl', 'echo', 'wsl'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'wsl' in result.stdout:
                return "wsl"
            else:
                return "windows"
        except Exception as e:
            return "windows"
    else:
        return os_type


def detect_os_for_testing():
    """테스트용 운영체제 감지 함수 - Windows로 강제 설정"""
    return "windows"


def get_backup_files_by_os():
    """운영체제에 따라 백업할 파일 목록을 반환"""
    os_type = detect_os()
    
    if os_type == "wsl" or os_type == "linux":
        # Linux/WSL 환경
        return [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.profile"),
            os.path.expanduser("~/.bash_profile"),
            os.path.expanduser("~/.bash_aliases"),
            os.path.expanduser("~/.inputrc"),
            os.path.expanduser("~/.vimrc"),
            os.path.expanduser("~/.gitconfig"),
            os.path.expanduser("~/.ssh/config"),
            os.path.expanduser("~/.tmux.conf")
        ]
    elif os_type == "windows":
        # Windows 환경 - bashrc, zshrc 제외
        return [
            os.path.expanduser("~/Documents/PowerShell/Microsoft.PowerShell_profile.ps1"),
            os.path.expanduser("~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1"),
            os.path.expanduser("~/.gitconfig"),
            os.path.expanduser("~/AppData/Roaming/Code/User/settings.json"),
            os.path.expanduser("~/AppData/Roaming/Code/User/keybindings.json"),
            os.path.expanduser("~/AppData/Roaming/Code/User/snippets"),
            os.path.expanduser("~/AppData/Roaming/Code/User/extensions"),
            os.path.expanduser("~/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json")
        ]
    else:
        # 기타 환경
        return []


def get_backup_directory_by_os():
    """운영체제에 따라 백업 디렉토리를 반환"""
    os_type = detect_os()
    
    if os_type == "wsl" or os_type == "linux":
        # Linux/WSL 환경
        return os.path.join(os.path.expanduser("~"), "Downloads", "pk_system", ".pk_system")
    elif os_type == "windows":
        # Windows 환경
        return os.path.join(os.path.expanduser("~"), "Downloads", "pk_system", ".pk_system")
    else:
        # 기타 환경
        return os.path.join(os.path.expanduser("~"), "Downloads", "pk_system", ".pk_system")


def ensure_bashrc_zshrc_backed_up():
    """bashrc와 zshrc 파일을 백업하는 함수"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'BACKUP_OS_DETECTED': '감지된 운영체제',
                'BACKUP_COMPLETE': '백업 완료',
                'BACKUP_FAILED': '백업 실패',
                'BACKUP_FILE_NOT_FOUND': '파일이 존재하지 않음',
                'BACKUP_TOTAL_COMPLETE': '총 백업 완료',
                'BACKUP_NO_FILES': '백업할 파일이 없습니다'
            })()

        import os
        import platform
        from datetime import datetime
        
        # 운영체제 감지
        os_type = platform.system()
        print(f"[{PkTexts.BACKUP_OS_DETECTED}] {PkColors.CYAN}OS={os_type} {PkColors.RESET}")
        
        # 백업할 파일 목록
        files_to_backup = []
        
        if os_type == "Linux" or os_type == "Darwin":  # Linux 또는 macOS
            home_dir = os.path.expanduser("~")
            potential_files = [
                os.path.join(home_dir, ".bashrc"),
                os.path.join(home_dir, ".zshrc"),
                os.path.join(home_dir, ".bash_profile"),
                os.path.join(home_dir, ".profile"),
                os.path.join(home_dir, ".bash_login")
            ]
        elif os_type == "Windows":
            home_dir = os.path.expanduser("~")
            potential_files = [
                os.path.join(home_dir, ".bashrc"),
                os.path.join(home_dir, ".zshrc"),
                os.path.join(home_dir, ".bash_profile")
            ]
        else:
            print(f"지원하지 않는 운영체제: {os_type}")
            return False
        
        # 존재하는 파일만 백업 목록에 추가
        for file_path in potential_files:
            if os.path.exists(file_path):
                files_to_backup.append(file_path)
        
        if not files_to_backup:
            print(f"[{PkTexts.BACKUP_NO_FILES}]")
            return False
        
        # 백업 실행
        backed_up_files = []
        for file_path in files_to_backup:
            try:
                # 백업 파일명 생성
                file_name = os.path.basename(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file_name = f"{file_name}.backup_{timestamp}"
                backup_path = os.path.join(os.path.dirname(file_path), backup_file_name)
                
                # 파일 복사
                import shutil
                shutil.copy2(file_path, backup_path)
                
                backed_up_files.append(backup_path)
                print(f"[{PkTexts.BACKUP_COMPLETE}] {PkColors.CYAN}파일={file_name} 백업={backup_file_name} {PkColors.RESET}")
                
            except Exception as e:
                print(f"[{PkTexts.BACKUP_FAILED}] {PkColors.RED}파일={file_path} 오류={str(e)} {PkColors.RESET}")
            except FileNotFoundError:
                print(f"[{PkTexts.BACKUP_FILE_NOT_FOUND}] {PkColors.YELLOW}파일={file_path} {PkColors.RESET}")
        
        # 결과 요약
        if backed_up_files:
            print(f"[{PkTexts.BACKUP_TOTAL_COMPLETE}] {PkColors.CYAN}총파일수={len(backed_up_files)}개 {PkColors.RESET}")
            return True
        else:
            print(f"[{PkTexts.BACKUP_NO_FILES}]")
            return False
            
    except Exception as e:
        print(f"[{PkTexts.BACKUP_FAILED}] {PkColors.RED}오류={e} {PkColors.RESET}")
        return False


if __name__ == "__main__":
    import sys
    
    # 명령행 인수에서 custom suffix 받기
    custom_suffix = None
    if len(sys.argv) > 1:
        custom_suffix = sys.argv[1]
        print(f" 사용자 정의 suffix 사용: {custom_suffix}")
    
    # 테스트 실행
    backed_up_files = ensure_bashrc_zshrc_backed_up(custom_suffix=custom_suffix)
    
    if backed_up_files:
        print(f" 총 {len(backed_up_files)}개 파일 백업 완료")
    else:
        print("️ 백업할 파일이 없습니다") 
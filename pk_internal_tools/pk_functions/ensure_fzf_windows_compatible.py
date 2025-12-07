"""
Windows에서 fzf 명령어를 안전하게 실행하기 위한 전용 함수들
"""

import os
import subprocess
import tempfile
from typing import List, Optional, Tuple


def run_fzf_windows_safe(input_data: str, fzf_options: Optional[List[str]] = None) -> Optional[str]:
    """
    Windows에서 fzf를 안전하게 실행하는 함수
    
    Args:
        input_data: fzf에 전달할 입력 데이터
        fzf_options: fzf 옵션 리스트
        
    Returns:
        선택된 결과 또는 None
    """
    if fzf_options is None:
        fzf_options = [
            "--height", "40%",
            "--layout", "reverse",
            "--border",
            "--preview", "echo {}",
            "--preview-window", "right:50%",
            "--bind", "ctrl-o:execute(echo 'OPEN_FILE_PATH')",
            "--bind", "ctrl-x:execute(echo 'OPEN_FILE')",
            "--header", "Ctrl+O: 파일 경로 열기 | Ctrl+X: 파일 열기 | Enter: 선택"
        ]
    
    # Windows에서 문제가 되는 옵션들 제거
    safe_options = []
    for option in fzf_options:
        if option not in ["--exit-0"]:  # Windows에서 문제가 되는 옵션 제외
            safe_options.append(option)
    
    try:
        # 방법 1: PowerShell을 통한 실행
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write(input_data)
        temp_file.close()
        
        # PowerShell 명령어 구성
        fzf_args = " ".join(safe_options)
        ps_cmd = f'''powershell -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; Get-Content '{temp_file.name}' -Encoding UTF8 | fzf {fzf_args}"'''
        
        result = subprocess.run(ps_cmd, shell=True, text=True, encoding='utf-8', capture_output=True)
        
        # 임시 파일 삭제
        try:
            os.unlink(temp_file.name)
        except:
            pass
            
        if result.returncode == 0:
            return result.stdout.strip()
            
    except Exception as e:
        print(f"PowerShell 방식 실패: {e}")
        
        try:
            # 방법 2: 직접 fzf 실행
            fzf_cmd = ["fzf"] + safe_options
            result = subprocess.run(
                fzf_cmd,
                input=input_data,
                text=True,
                encoding='utf-8',
                capture_output=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
                
        except Exception as e2:
            print(f"직접 fzf 실행도 실패: {e2}")
    
    return None


def run_fzf_windows_interactive(input_data: str, fzf_options: Optional[List[str]] = None) -> Tuple[int, str, str]:
    """
    Windows에서 fzf를 대화형으로 실행하는 함수
    
    Args:
        input_data: fzf에 전달할 입력 데이터
        fzf_options: fzf 옵션 리스트
        
    Returns:
        (returncode, stdout, stderr) 튜플
    """
    if fzf_options is None:
        fzf_options = [
            "--height", "40%",
            "--layout", "reverse",
            "--border",
            "--preview", "echo {}",
            "--preview-window", "right:50%",
            "--bind", "ctrl-o:execute(echo 'OPEN_FILE_PATH')",
            "--bind", "ctrl-x:execute(echo 'OPEN_FILE')",
            "--header", "Ctrl+O: 파일 경로 열기 | Ctrl+X: 파일 열기 | Enter: 선택"
        ]
    
    # Windows에서 문제가 되는 옵션들 제거
    safe_options = []
    for option in fzf_options:
        if option not in ["--exit-0"]:  # Windows에서 문제가 되는 옵션 제외
            safe_options.append(option)
    
    try:
        # PowerShell을 통한 대화형 실행
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write(input_data)
        temp_file.close()
        
        # PowerShell 명령어 구성
        fzf_args = " ".join(safe_options)
        ps_cmd = f'''powershell -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; Get-Content '{temp_file.name}' -Encoding UTF8 | fzf {fzf_args}"'''
        
        result = subprocess.run(ps_cmd, shell=True, text=True, encoding='utf-8')
        
        # 임시 파일 삭제
        try:
            os.unlink(temp_file.name)
        except:
            pass
            
        return result.returncode, result.stdout, result.stderr
            
    except Exception as e:
        print(f"PowerShell 대화형 실행 실패: {e}")
        
        try:
            # 직접 fzf 대화형 실행
            fzf_cmd = ["fzf"] + safe_options
            result = subprocess.run(
                fzf_cmd,
                input=input_data,
                text=True,
                encoding='utf-8'
            )
            
            return result.returncode, result.stdout, result.stderr
                
        except Exception as e2:
            print(f"직접 fzf 대화형 실행도 실패: {e2}")
            return 1, "", str(e2)
    
    return 1, "", "Unknown error"


def is_fzf_available() -> bool:
    """fzf가 사용 가능한지 확인"""
    try:
        result = subprocess.run(["fzf", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def get_fzf_version() -> Optional[str]:
    """fzf 버전 정보 반환"""
    try:
        result = subprocess.run(["fzf", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None 
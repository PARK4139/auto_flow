#!/usr/bin/env python3
"""
명령어 실행 함수 - 인코딩 문제 및 오류 처리 개선
"""

import subprocess
import traceback
from pathlib import Path


def run_command(cmd: str, capture_output=False):
    """
    명령어를 실행하는 함수
    
    Args:
        cmd: 실행할 명령어
        capture_output: 출력을 캡처할지 여부
    
    Returns:
        tuple: (returncode, output) 또는 (returncode, "")
    """
    try:
        if capture_output:
            # 인코딩 문제 해결을 위해 encoding 명시적 설정
            result = subprocess.run(
                cmd, 
                shell=True, 
                text=True, 
                capture_output=True,
                encoding='utf-8',  # 명시적 인코딩 설정
                errors='replace'    # 디코딩 오류 시 대체 문자 사용
            )
            
            # stdout과 stderr이 None일 수 있으므로 안전하게 처리
            stdout = result.stdout if result.stdout is not None else ""
            stderr = result.stderr if result.stderr is not None else ""
            
            return result.returncode, stdout + stderr
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode, ""
            
    except Exception as exception:
        # 예외 발생 시 로그 출력
        print(f"명령어 실행 중 오류 발생: {cmd}")
        print(f"오류 내용: {str(exception)}")
        traceback.print_exc()
        
        # 오류 발생 시에도 기본값 반환
        return -1, f"오류 발생: {str(exception)}"
    
    except UnicodeDecodeError as decode_error:
        # 인코딩 오류 특별 처리
        print(f"인코딩 오류 발생: {cmd}")
        print(f"인코딩 오류 내용: {str(decode_error)}")
        
        # 인코딩 오류 시에도 기본값 반환
        return -1, f"인코딩 오류: {str(decode_error)}"


def run_command_safe(cmd: str, capture_output=False):
    """
    안전한 명령어 실행 함수 (추가 안전장치)
    
    Args:
        cmd: 실행할 명령어
        capture_output: 출력을 캡처할지 여부
    
    Returns:
        tuple: (returncode, output) 또는 (returncode, "")
    """
    try:
        return run_command(cmd, capture_output)
    except Exception as e:
        print(f"run_command_safe에서 예외 발생: {str(e)}")
        return -1, f"안전 실행 실패: {str(e)}"


# 사용 예제
if __name__ == "__main__":
    # 테스트 실행
    print("=== run_command 테스트")
    
    # n. 기본 명령어 실행
    code, output = run_command("echo Hello World")
    print(f"기본 실행: code={code}, output='{output}'")
    
    # n. 출력 캡처 테스트
    code, output = run_command("dir", capture_output=True)
    print(f"출력 캡처: code={code}, output 길이={len(output)}")
    
    # n. 오류 명령어 테스트
    code, output = run_command("nonexistent_command", capture_output=True)
    print(f"오류 명령어: code={code}, output='{output}'")

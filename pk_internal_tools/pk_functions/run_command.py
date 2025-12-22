#!/usr/bin/env python3
"""
명령어 실행 함수 - 인코딩 문제 및 오류 처리 개선
"""

import subprocess
import traceback


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
                errors='replace'  # 디코딩 오류 시 대체 문자 사용
            )

            # stdout과 stderr이 None일 수 있으므로 안전하게 처리
            stdout = result.stdout if result.stdout is not None else ""
            stderr = result.stderr if result.stderr is not None else ""

            return result.returncode, stdout + stderr
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode, ""

    except Exception as e:
        # 예외 발생 시 로그 출력
        print(f"명령어 실행 중 오류 발생: {cmd}")
        print(f"오류 내용: {str(e)}")
        traceback.print_exc()

        # 오류 발생 시에도 기본값 반환
        return -1, f"오류 발생: {str(e)}"

    except UnicodeDecodeError as decode_error:
        # 인코딩 오류 특별 처리
        print(f"인코딩 오류 발생: {cmd}")
        print(f"인코딩 오류 내용: {str(decode_error)}")

        # 인코딩 오류 시에도 기본값 반환
        return -1, f"인코딩 오류: {str(decode_error)}"

#!/usr/bin/env python3
"""
다음 커밋 번호를 가져오는 함수 - 안전한 오류 처리 추가
"""

import re
from pk_internal_tools.pk_functions.run_command import run_command


def get_next_commit_number():
    """
    Git 로그에서 다음 커밋 번호를 계산하는 함수
    
    Returns:
        int: 다음 커밋 번호
    """
    try:
        # Git 로그 가져오기 (pager 비활성화)
        result = run_command('git --no-pager log -n 20 --pretty=format:"%s"', capture_output=True)
        
        # run_command가 None을 반환할 수 있으므로 안전하게 처리
        if result is None:
            print("️  run_command가 None을 반환했습니다. 기본값 1을 사용합니다.")
            return 1
        
        code, log_output = result
        
        # Git 명령어 실패 시
        if code != 0:
            print(f"️  Git 명령어 실패 (code: {code}). 기본값 1을 사용합니다.")
            return 1
        
        # log_output이 None이거나 빈 문자열인 경우
        if not log_output:
            print("️  Git 로그 출력이 비어있습니다. 기본값 1을 사용합니다.")
            return 1
        
        # 커밋 번호 추출 - 개선된 로직
        numbers = []
        commit_count = 0
        
        print(f"🔧 Git 로그 분석 중... (총 {len(log_output.splitlines())}개 라인)")
        
        for line in log_output.splitlines():
            line = line.strip()
            if line:  # 빈 줄 건너뛰기
                commit_count += 1
                print(f"🔧 커밋 {commit_count}: {line[:50]}...")  # 디버깅용
                
                # 방법 1: [숫자] 형식 찾기
                match = re.search(r"\[(\d+)\]", line)
                if match:
                    try:
                        number = int(match.group(1))
                        numbers.append(number)
                        print(f"🔧 [숫자] 형식 발견: {number}")
                        continue
                    except ValueError:
                        pass
        
        # [숫자] 형식이 없으면 커밋 개수 기반으로 번호 생성
        if not numbers:
            print(f"🔧 [숫자] 형식의 커밋 번호를 찾을 수 없습니다.")
            print(f"🔧 총 {commit_count}개의 커밋을 발견했습니다.")
            # 간단하게 커밋 개수 + 1을 반환
            next_number = commit_count + 1
            print(f"🔧 커밋 개수 기반 다음 번호: {next_number}")
            return next_number
        
        next_number = max(numbers) + 1
        print(f"🔧 다음 커밋 번호 계산 완료: {next_number} (발견된 번호들: {numbers})")
        return next_number
        
    except Exception as e:
        print(f" get_next_commit_number에서 오류 발생: {str(e)}")
        print("기본값 1을 사용합니다.")
        return 1


def get_next_commit_number_safe():
    """
    안전한 커밋 번호 가져오기 함수 (추가 안전장치)
    
    Returns:
        int: 다음 커밋 번호
    """
    try:
        return get_next_commit_number()
    except Exception as e:
        print(f" get_next_commit_number_safe에서 예외 발생: {str(e)}")
        return 1


# 사용 예제
if __name__ == "__main__":
    print("=== get_next_commit_number 테스트")
    
    try:
        next_number = get_next_commit_number()
        print(f"다음 커밋 번호: {next_number}")
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")
        print("기본값 1을 사용합니다.")
        next_number = 1
    
    print(f"최종 커밋 번호: {next_number}")



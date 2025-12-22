#!/usr/bin/env python3
"""
다음 커밋 번호를 가져오는 함수 - 안전한 오류 처리 추가
"""

import logging
import re
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def get_next_commit_number():
    """
    Git 로그에서 다음 커밋 번호를 계산하는 함수
    
    Returns:
        int: 다음 커밋 번호
    """
    try:
        # Git 로그 가져오기 (pager 비활성화)
        stdout_lines, stderr_lines, code = ensure_command_executed(
            'git --no-pager log -n 20 --pretty=format:"%s"',
            mode_silent=True
        )
        log_output = "\n".join(stdout_lines + stderr_lines)

        # Git 명령어 실패 시
        if code != 0:
            logging.warning(f"Git command failed (code: {code}). Using 1 as default.")
            return 1
        
        # log_output이 None이거나 빈 문자열인 경우
        if not log_output:
            logging.warning("Git log output is empty. Using 1 as default.")
            return 1
        
        # 커밋 번호 추출 - 개선된 로직
        numbers = []
        commit_count = 0
        
        logging.debug(f"Analyzing Git log... (Total {len(log_output.splitlines())} lines)")
        
        for line in log_output.splitlines():
            line = line.strip()
            if line:  # 빈 줄 건너뛰기
                commit_count += 1
                logging.debug(f"Commit {commit_count}: {line[:50]}...")
                
                # 방법 1: [숫자] 형식 찾기
                match = re.search(r"\[(\d+)\]", line)
                if match:
                    try:
                        number = int(match.group(1))
                        numbers.append(number)
                        logging.debug(f"Found [number] format: {number}")
                        continue
                    except ValueError:
                        pass
        
        # [숫자] 형식이 없으면 커밋 개수 기반으로 번호 생성
        if not numbers:
            logging.debug(f"Could not find commit number in [number] format.")
            logging.debug(f"Found {commit_count} total commits.")
            # 간단하게 커밋 개수 + 1을 반환
            next_number = commit_count + 1
            logging.debug(f"Next number based on commit count: {next_number}")
            return next_number
        
        next_number = max(numbers) + 1
        logging.debug(f"Next commit number calculated: {next_number} (Found numbers: {numbers})")
        return next_number
        
    except Exception as e:
        logging.error(f"Error in get_next_commit_number: {str(e)}")
        logging.warning("Using 1 as default.")
        return 1

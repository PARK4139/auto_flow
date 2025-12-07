
import os
import sys
def is_in_venv():
    if "VIRTUAL_ENV" in os.environ:
        # virtual environment 에서 실행 중입니다.
        some_condition = 1
        print(some_condition)
        # sys.exit(0)  # %errorlevel%=0  # 성공
        return True
    else:
        # virtual environment 이 아닙니다.
        some_condition = 0
        print(some_condition)
        # sys.exit(1)  # %errorlevel%=1  # 실패
        return False
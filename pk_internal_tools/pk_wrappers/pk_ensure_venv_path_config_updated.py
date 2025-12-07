import os
import time
from datetime import datetime

import logging

# 수정 대상 디렉토리 설정 (OS별 virtual environment 경로)
import platform
if platform.system().lower() == "windows":
    target_dir = os.path.expanduser(r'~\Downloads\pk_system\.venv')
else:
    target_dir = os.path.expanduser(r'~\Downloads\pk_system\.venv')

# USERPROFILE 경로 가져오기
user_profile_path = os.getenv('USERPROFILE')


# 경로 수정할 함수
def replace_path_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 파일 내용 수정
        new_lines = []
        for line in lines:
            line = line.replace(r'%USERPROFILE%', user_profile_path)
            line = line.replace(r'C:\Users\wjdgns', user_profile_path)
            new_lines.append(line)

        # 수정된 내용을 원본 파일로 덮어쓰기
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

        return True  # 파일 처리 성공
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False  # 파일 처리 실패


# 파일 처리 함수
def process_files():
    # 수정 대상 파일 수를 계산
    file_count = 0
    for root, dirs, files in os.walk(target_dir):
        file_count += len(files)

    # 수정 대상 파일 수 출력
    logging.debug(f"Total number of files to process: {file_count}")

    # 작업 시작 타임스탬프
    start_time = time.time()
    start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.debug(f"Task started at: {start_timestamp}")


    # OS별 virtual environment 디렉토리 내 모든 파일 순회
    processed_count = 0
    for root, dirs, files in os.walk(target_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if replace_path_in_file(file_path):
                logging.debug(f"[SUCCESS] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {file_path}")
            else:
                logging.warning(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {file_path}")
            processed_count += 1

    # 작업 종료 타임스탬프 및 시간 계산
    end_time = time.time()
    end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elapsed_time = end_time - start_time

    # 작업 종료 정보 출력
    # print("All files have been successfully modified.")
    # print(f"Task started at: {start_timestamp}")
    # print(f"Task ended at: {end_timestamp}")
    # print(f"Total time taken: {elapsed_time:.2f} seconds")
    # print(f"Total files processed: {processed_count}")
    print("모든 파일이 성공적으로 수정되었습니다.")
    print(f"작업 시작 시간: {start_timestamp}")
    print(f"작업 종료 시간: {end_timestamp}")
    print(f"총 소요 시간: {elapsed_time:.2f} 초")
    print(f"처리된 파일 수: {processed_count}")


# exec
if __name__ == "__main__":
    process_files()

    input("\nPress Enter to exit...")

# import os
#
# # 수정 대상 디렉토리 설정
# target_dir = os.path.expanduser(r'~\Downloads\pk_system\.venv')
#
# # USERPROFILE 경로 가져오기
# user_profile_path = os.getenv('USERPROFILE')
#
# # 경로 수정할 함수
# def replace_path_in_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     # 파일 내용 수정
#     new_lines = []
#     for line in lines:
#         line = line.replace(r'%USERPROFILE%', user_profile_path)
#         line = line.replace(r'C:\Users\wjdgns', user_profile_path)
#         new_lines.append(line)
#
#     # 수정된 내용을 원본 파일로 덮어쓰기
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.writelines(new_lines)
#
# # 파일 처리 함수
# def process_files():
#     # .venv 디렉토리 내 모든 파일 순회
#     for root, dirs, files in os.walk(target_dir):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             print(f"Processing file: {file_path}")
#             replace_path_in_file(file_path)
#
#     print("All files have been successfully modified.")
#
# # exec 
# if __name__ == "__main__":
#     process_files()
#
#     input("\nPress Enter to exit...")

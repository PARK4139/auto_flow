import os
import sys

# from pk_internal_tools.pk_objects.static_logic import D_PK_WORKING

# colorama 설정 (Windows에서 색상 출력 지원)
try:
    from colorama import init, Fore
    init(autoreset=True)  # 자동 리셋 설정
except ImportError:
    print("[ERROR] colorama 라이브러리가 설치되어 있지 않습니다. 'pip install colorama'를 exec 하세요.")
    sys.exit(1)

# [OPTION]
# d_working = r"D:\pkg_classified"
d_working = D_PK_WORKING

def print_debug(message):
    """디버깅 메시지 출력 (회색)"""
    print(f"{Fore.LIGHTBLACK_EX}[DEBUG] {message}")

def print_error(message):
    """오류 메시지 출력 (빨간색)"""
    print(f"{Fore.RED}[ERROR] {message}")

def print_info(message):
    """일반 정보 메시지 출력 (파란색)"""
    print(f"{Fore.BLUE}[INFO] {message}")

def rename_d_list(d_working):
    """ 지정된 디렉토리 내에서 pkg_ 및 mkr_ 접두사를 제거하고 [ ]로 묶어 이름 변경 """
    if not os.path.exists(d_working):
        print_error(f"대상 디렉토리가 존재하지 않습니다: {d_working}")
        return

    for folder in os.listdir(d_working):
        old_path = os.path.join(d_working, folder)

        if not os.path.isdir(old_path):  # 폴더만 처리
            continue

        new_name = folder.replace("pkg_", "").replace("mkr_", "")

        # 이미 [ ] 로 묶여 있으면 변경하지 않음
        if new_name.startswith("[") and new_name.endswith("]"):
            print_debug(f"'{folder}' 이미 [ ] 형태라 변경하지 않음")
            continue
        
        new_name = f"[{new_name}]"
        new_path = os.path.join(d_working, new_name)

        # 중복 방지: 동일한 이름의 폴더가 존재하는 경우 변경하지 않음
        if os.path.exists(new_path):
            print_error(f"변경 불가: '{folder}' → '{new_name}' (이미 존재함)")
            continue

        # 폴더 이름 변경
        os.rename(old_path, new_path)
        print_info(f"'{folder}' → '{new_name}' 변경 완료")

    print_info("모든 디렉토리 이름 변경 작업 완료!")

if __name__ == "__main__":
    rename_d_list(d_working)

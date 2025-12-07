import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

def ensure_uv_enabled():
    """자동으로 uv를 설치하고 PATH에 등록"""
    # 이미 설치되어 있는지 확인
    uv_exe = shutil.which("uv")
    if uv_exe:
        print(f" 'uv' already installed: {uv_exe}")
        subprocess.run(["uv", "--version"])
        return

    print(" 'uv' 설치를 시작합니다...")

    system = platform.system().lower()
    arch = platform.machine().lower()

    # 플랫폼에 맞는 다운로드 URL 설정
    if system == "windows":
        url = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"
        uv_executable_name = "uv.exe"
    elif system == "linux":
        url = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz"
        uv_executable_name = "uv"
    elif system == "darwin":
        url = "https://github.com/astral-sh/uv/releases/latest/download/uv-aarch64-apple-darwin.tar.gz" if "arm" in arch else \
              "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-apple-darwin.tar.gz"
        uv_executable_name = "uv"
    else:
        raise Exception(f" 지원되지 않는 플랫폼: {system}")

    # 다운로드 및 압축 해제
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, os.path.basename(url))
        print(f" 다운로드 중: {url}")
        urllib.request.urlretrieve(url, zip_path)

        extract_dir = os.path.join(tmpdir, "uv_extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if url.endswith(".zip"):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
        elif url.endswith(".tar.gz"):
            import tarfile
            with tarfile.open(zip_path, "r:gz") as tar:
                tar.extractall(extract_dir)
        else:
            raise Exception(" 알 수 없는 압축 형식")

        # 실행 파일 찾기
        uv_path = None
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f == uv_executable_name:
                    uv_path = os.path.join(root, f)
                    break

        if not uv_path or not os.path.exists(uv_path):
            raise Exception(" uv 실행 파일을 찾을 수 없습니다")

        # 현재 작업 디렉토리에 복사
        final_path = os.path.join(os.getcwd(), uv_executable_name)
        shutil.move(uv_path, final_path)
        print(f" 'uv' 설치 완료: {final_path}")

        if system != "windows":
            os.chmod(final_path, 0o755)

        # PATH 등록 시도
        try:
            if system == "windows":
                add_to_path_windows(os.getcwd())
            else:
                add_to_path_unix(os.getcwd())
        except Exception as e:
            print(f"️ PATH 등록 중 오류 발생: {e}")

        # 버전 확인
        subprocess.run([final_path, "--version"])

        print(" 'uv' 설치 및 등록이 완료되었습니다!")

# Windows PATH 등록 (레지스트리 사용)
def add_to_path_windows(dir_to_add):
    import winreg

    print(" Windows PATH 등록 중...")

    # 현재 사용자 환경변수 PATH 읽기
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as key:
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""

    # 중복 방지
    if dir_to_add.lower() in current_path.lower():
        print(f" 이미 PATH에 등록됨: {dir_to_add}")
        return

    new_path = f"{current_path};{dir_to_add}" if current_path else dir_to_add

    # 환경변수 쓰기
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

    print(f" Windows 사용자 PATH에 등록 완료: {dir_to_add}")
    print("️ 변경 사항은 새 콘솔에서 적용됩니다.")

# Linux/macOS PATH 등록 (~/.bashrc)
def add_to_path_unix(dir_to_add):
    bashrc_path = os.path.expanduser("~/.bashrc")
    export_line = f'\n# [uv 자동 설치]\nexport PATH="{dir_to_add}:$PATH"\n'

    with open(bashrc_path, "a") as f:
        f.write(export_line)

    print(f" ~/.bashrc에 PATH 추가 완료: {dir_to_add}")
    print("️ 변경 사항은 새로운 터미널 세션에서 적용됩니다.")

if __name__ == "__main__":
    ensure_uv_enabled()

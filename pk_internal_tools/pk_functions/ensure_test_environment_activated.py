#!/usr/bin/env python3
"""
테스트 환경 자동 활성화 및 테스트 실행 스크립트
OS 환경에 따라 적절한 virtual environment 을 자동으로 활성화하고 테스트를 실행
"""

import os
import sys
import platform
import subprocess
import logging
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_environment.log', encoding='utf-8')
        ]
    )

def detect_os_environment() -> Dict[str, Any]:
    """OS 환경 감지"""
    system = platform.system().lower()
    is_wsl = "microsoft" in platform.uname().release.lower() if hasattr(platform, 'uname') else False
    
    env_info = {
        "os": system,
        "is_wsl": is_wsl,
        "is_windows": system == "windows",
        "is_linux": system == "linux",
        "is_macos": system == "darwin",
        "python_version": sys.version,
        "python_executable": sys.executable
    }
    
    logging.debug(f"OS 환경 감지: {env_info}")
    return env_info

def find_virtual_environment(env_info: Dict[str, Any]) -> Optional[Path]:
    """virtual environment 디렉토리 찾기"""
    project_root = Path(__file__).parent.parent.parent
    
    # Windows 환경
    if env_info["is_windows"]:
        venv_paths = [
            project_root / ".venv",
            project_root / "venv",
            project_root / "env"
        ]
    # Linux/WSL 환경
    else:
        venv_paths = [
            project_root / ".venv",
            project_root / ".venv",
            project_root / "venv",
            project_root / "env"
        ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            logging.debug(f"virtual environment 발견: {venv_path}")
            return venv_path
    
    logging.warning("virtual environment 을 찾을 수 없음")
    return None

def find_python_executable(env_info: Dict[str, Any]) -> Optional[str]:
    """Python 실행 파일 찾기"""
    python_commands = []
    
    # Windows 환경
    if env_info["is_windows"]:
        python_commands = ["python", "python3", "py"]
    # Linux/WSL 환경
    else:
        python_commands = ["python3", "python", "uv"]
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logging.debug(f"Python 실행 파일 발견: {cmd}")
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    logging.warning("Python 실행 파일을 찾을 수 없음")
    return None

def activate_virtual_environment(venv_path: Path, env_info: Dict[str, Any]) -> bool:
    """virtual environment 활성화"""
    try:
        if env_info["is_windows"]:
            # Windows 환경
            activate_script = venv_path / "Scripts" / "activate.bat"
            if activate_script.exists():
                logging.debug(f"Windows virtual environment 활성화: {activate_script}")
                # 환경 변수 설정
                os.environ["VIRTUAL_ENV"] = str(venv_path)
                os.environ["PATH"] = f"{venv_path}\\Scripts;{os.environ['PATH']}"
                return True
        else:
            # Linux/WSL 환경
            activate_script = venv_path / "bin" / "activate"
            if activate_script.exists():
                logging.debug(f"Linux/WSL virtual environment 활성화: {activate_script}")
                # 환경 변수 설정
                os.environ["VIRTUAL_ENV"] = str(venv_path)
                os.environ["PATH"] = f"{venv_path}/bin:{os.environ['PATH']}"
                return True
        
        logging.warning(f"virtual environment 활성화 스크립트를 찾을 수 없음: {venv_path}")
        return False
        
    except Exception as e:
        logging.error(f"virtual environment 활성화 실패: {str(e)}")
        return False

def install_dependencies(python_cmd: str, env_info: Dict[str, Any]) -> bool:
    """의존성 설치"""
    try:
        project_root = Path(__file__).parent.parent.parent
        
        # uv.lock 파일이 있으면 uv sync --active 사용
        if (project_root / "uv.lock").exists():
            logging.debug("uv.lock 파일 발견 - uv sync --active 실행")
            if env_info["is_windows"]:
                result = subprocess.run(["uv", "sync", "--active", "-vvv"],
                                      cwd=project_root, 
                                      capture_output=True, text=True, timeout=60)
            else:
                result = subprocess.run(["uv", "sync", "--active", "-vvv"],
                                      cwd=project_root, 
                                      capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logging.debug("uv sync --active 성공")
                return True
            else:
                logging.warning(f"uv sync --active 실패: {result.stderr}")
        
        # requirements.txt 파일이 있으면 pip install 사용
        requirements_file = project_root / "requirements.txt"
        if requirements_file.exists():
            logging.debug("requirements.txt 파일 발견 - pip install 실행")
            result = subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  cwd=project_root, 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logging.debug("pip install 성공")
                return True
            else:
                logging.warning(f"pip install 실패: {result.stderr}")
        
        # pyproject.toml 파일이 있으면 pip install -e 사용
        pyproject_file = project_root / "pyproject.toml"
        if pyproject_file.exists():
            logging.debug("pyproject.toml 파일 발견 - pip install -e 실행")
            result = subprocess.run([python_cmd, "-m", "pip", "install", "-e", "."], 
                                  cwd=project_root, 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logging.debug("pip install -e 성공")
                return True
            else:
                logging.warning(f"pip install -e 실패: {result.stderr}")
        
        logging.debug("의존성 설치 파일을 찾을 수 없음 - 건너뜀")
        return True
        
    except Exception as e:
        logging.error(f"의존성 설치 실패: {str(e)}")
        return False

def run_test(test_file: str, python_cmd: str, env_info: Dict[str, Any]) -> bool:
    """테스트 실행"""
    try:
        test_path = Path(test_file)
        if not test_path.exists():
            logging.error(f"테스트 파일을 찾을 수 없음: {test_file}")
            return False
        
        logging.debug(f"테스트 실행 시작: {test_file}")
        logging.debug(f"Python 명령어: {python_cmd}")
        logging.debug(f"현재 작업 디렉토리: {Path.cwd()}")
        
        # 테스트 실행
        result = subprocess.run([python_cmd, str(test_path)], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logging.debug("테스트 실행 성공")
            if result.stdout:
                logging.debug(f"테스트 출력:\n{result.stdout}")
            return True
        else:
            logging.error(f"테스트 실행 실패 (종료 코드: {result.returncode})")
            if result.stderr:
                logging.error(f"오류 출력:\n{result.stderr}")
            if result.stdout:
                logging.debug(f"표준 출력:\n{result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error("테스트 실행 시간 초과 (5분)")
        return False
    except Exception as e:
        logging.error(f"테스트 실행 중 오류 발생: {str(e)}")
        return False

def main():
    """메인 함수"""
    setup_logging()
    
    logging.debug("테스트 환경 자동 활성화 시작")
    
    # n. OS 환경 감지
    env_info = detect_os_environment()
    
    # n. virtual environment 찾기
    venv_path = find_virtual_environment(env_info)
    
    # n. Python 실행 파일 찾기
    python_cmd = find_python_executable(env_info)
    if not python_cmd:
        logging.error("Python 실행 파일을 찾을 수 없음")
        return False
    
    # n. virtual environment 활성화 (가능한 경우)
    if venv_path:
        if activate_virtual_environment(venv_path, env_info):
            logging.debug("virtual environment 활성화 완료")
        else:
            logging.warning("virtual environment 활성화 실패 - 시스템 Python 사용")
    else:
        logging.debug("virtual environment 없음 - 시스템 Python 사용")
    
    # n. 의존성 설치
    if not install_dependencies(python_cmd, env_info):
        logging.warning("의존성 설치 실패 - 계속 진행")
    
    # 6. 테스트 파일 실행 (명령행 인수로 받음)
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        success = run_test(test_file, python_cmd, env_info)
        return success
    else:
        # 기본 테스트 파일들 실행
        default_tests = [
            "ensure_losslesscut_pk_event_test.py"
        ]
        
        all_success = True
        for test_file in default_tests:
            if Path(test_file).exists():
                success = run_test(test_file, python_cmd, env_info)
                all_success = all_success and success
            else:
                logging.warning(f"기본 테스트 파일을 찾을 수 없음: {test_file}")
        
        return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

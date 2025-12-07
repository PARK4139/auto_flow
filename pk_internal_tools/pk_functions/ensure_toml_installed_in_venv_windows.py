#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.venv virtual environment 에 toml 모듈을 자동으로 설치하는 함수

사용법:
    from pk_internal_tools.pk_functions.ensure_toml_installed_in_venv_windows import ensure_toml_installed_in_venv_windows
    ensure_toml_installed_in_venv_windows()
"""

import subprocess
import sys
from pathlib import Path
import logging
from typing import Optional

def ensure_toml_installed_in_venv_windows(force_reinstall: bool = False) -> bool:
    """
    .venv virtual environment 에 toml 모듈을 자동으로 설치합니다.
    
    Args:
        force_reinstall (bool): True이면 이미 설치되어 있어도 재설치
        
    Returns:
        bool: 설치 성공 여부
    """
    
    # 프로젝트 루트 디렉토리 찾기
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir
    while project_root.parent != project_root:
        if (project_root / "pyproject.toml").exists():
            break
        project_root = project_root.parent
    
    # .venv 경로 설정
    venv_windows = project_root / ".venv"
    python_exe = venv_windows / "Scripts" / "python.exe"
    pip_exe = venv_windows / "Scripts" / "pip.exe"
    
    # virtual environment 존재 확인
    if not python_exe.exists():
        logging.error(f".venv virtual environment 을 찾을 수 없습니다: {python_exe}")
        print(f"❌ .venv virtual environment 을 찾을 수 없습니다: {python_exe}")
        return False
    
    print(f"📁 .venv virtual environment 경로: {venv_windows}")
    print(f"🐍 Python 실행파일: {python_exe}")
    
    # Python 버전 확인
    try:
        result = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            python_version = result.stdout.strip()
            print(f"✅ Python 버전: {python_version}")
        else:
            print(f"⚠️ Python 버전 확인 실패")
    except Exception as e:
        print(f"⚠️ Python 버전 확인 중 오류: {e}")
    
    # toml 모듈 설치 상태 확인
    if not force_reinstall:
        try:
            result = subprocess.run(
                [str(python_exe), "-c", "import toml; print('OK:', toml.__version__)"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "OK:" in result.stdout:
                version = result.stdout.strip().replace("OK: ", "")
                print(f"✅ toml 모듈이 이미 설치되어 있습니다 (버전: {version})")
                return True
        except Exception as e:
            logging.debug(f"toml 모듈 확인 중 예외: {e}")
    
    # toml 모듈 설치
    print("📦 toml 모듈 설치를 시작합니다...")
    
    # 설치 방법들 (우선순위 순서)
    install_methods = [
        # n. uv pip 사용 (가장 빠름)
        {
            "name": "uv pip",
            "cmd": ["uv", "pip", "install", "toml", "--python", str(python_exe)],
            "timeout": 60
        },
        # n. 일반 pip 사용
        {
            "name": "pip",
            "cmd": [str(pip_exe), "install", "toml"],
            "timeout": 120
        },
        # n. python -m pip 사용
        {
            "name": "python -m pip",
            "cmd": [str(python_exe), "-m", "pip", "install", "toml"],
            "timeout": 120
        }
    ]
    
    # 각 방법을 순서대로 시도
    for method in install_methods:
        try:
            print(f"🔧 {method['name']}를 사용하여 설치 시도...")
            
            result = subprocess.run(
                method["cmd"],
                capture_output=True,
                text=True,
                timeout=method["timeout"]
            )
            
            if result.returncode == 0:
                print(f"✅ {method['name']}를 사용한 설치 성공!")
                print(f"   STDOUT: {result.stdout[:200]}...")
                
                # 설치 확인
                verify_result = subprocess.run(
                    [str(python_exe), "-c", "import toml; print('설치 확인:', toml.__version__)"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if verify_result.returncode == 0:
                    version = verify_result.stdout.strip().replace("설치 확인: ", "")
                    print(f"🎉 toml 모듈 설치 및 확인 완료! (버전: {version})")
                    return True
                else:
                    print(f"⚠️ 설치는 성공했지만 import 확인 실패")
                    continue
                    
            else:
                print(f"❌ {method['name']} 설치 실패:")
                print(f"   STDERR: {result.stderr[:200]}...")
                continue
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {method['name']} 설치 시간 초과 ({method['timeout']}초)")
            continue
        except FileNotFoundError:
            print(f"🚫 {method['name']} 명령어를 찾을 수 없음")
            continue
        except Exception as e:
            print(f"❌ {method['name']} 설치 중 오류: {e}")
            continue
    
    # 모든 방법 실패
    print("❌ 모든 설치 방법이 실패했습니다.")
    logging.error("toml 모듈 설치 실패 - 모든 방법 시도 완료")
    return False


def main():
    """메인 실행 함수"""
    print("=== .venv virtual environment toml 모듈 자동 설치")

    # 강제 재설치 옵션 확인
    force_reinstall = "--force" in sys.argv or "-f" in sys.argv
    if force_reinstall:
        print("🔄 강제 재설치 모드가 활성화되었습니다.")
    
    # 설치 실행
    success = ensure_toml_installed_in_venv_windows(force_reinstall=force_reinstall)
    
    if success:
        print("✅ 작업이 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print("❌ 작업이 실패했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()

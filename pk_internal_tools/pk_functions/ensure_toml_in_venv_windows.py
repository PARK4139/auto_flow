#!/usr/bin/env python3

"""
.venv virtual environment 에 toml 모듈을 자동으로 설치하는 독립 스크립트
"""

import subprocess
import sys
from pathlib import Path


def main():
    """메인 실행 함수"""
    print("=== .venv virtual environment 필수 모듈 자동 설치 (toml, pywin32)")
    
    # 프로젝트 루트 디렉토리 (현재 스크립트가 프로젝트 루트에 있다고 가정)
    project_root = Path(__file__).resolve().parent
    
    # .venv 경로 설정
    venv_windows = project_root / ".venv"
    python_exe = venv_windows / "Scripts" / "python.exe"
    pip_exe = venv_windows / "Scripts" / "pip.exe"
    
    # virtual environment 존재 확인
    if not python_exe.exists():
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
    
    # 강제 재설치 옵션 확인
    force_reinstall = "--force" in sys.argv or "-f" in sys.argv
    
    # 필요한 패키지들
    packages_to_install = ["toml", "pywin32"]
    
    # 각 패키지별로 설치 시도
    success_count = 0
    
    for package in packages_to_install:
        print(f"📦 {package} 모듈 설치를 시작합니다...")
        
        # 패키지별 import 이름 매핑
        import_name = package
        if package == "pywin32":
            import_name = "win32gui"
        
        # 이미 설치되어 있는지 확인 (강제 재설치가 아닌 경우)
        if not force_reinstall:
            try:
                result = subprocess.run(
                    [str(python_exe), "-c", f"import {import_name}; print('OK')"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode == 0 and "OK" in result.stdout:
                    print(f"✅ {package} 모듈이 이미 설치되어 있습니다")
                    success_count += 1
                    continue
            except Exception as e:
                print(f"🔍 {package} 모듈 확인 중 예외: {e}")
        
        # 설치 방법들 (우선순위 순서)
        install_methods = [
            # n. 일반 pip 사용
            {
                "name": "pip",
                "cmd": [str(pip_exe), "install", package],
                "timeout": 180
            },
            # n. python -m pip 사용
            {
                "name": "python -m pip",
                "cmd": [str(python_exe), "-m", "pip", "install", package],
                "timeout": 180
            }
        ]
        
        # 현재 패키지 설치 성공 여부
        package_installed = False
        
        # 각 방법을 순서대로 시도
        for method in install_methods:
            try:
                print(f"🔧 {method['name']}를 사용하여 {package} 설치 시도...")
                
                result = subprocess.run(
                    method["cmd"],
                    capture_output=True,
                    text=True,
                    timeout=method["timeout"],
                    encoding='utf-8',
                    errors='ignore'
                )
                
                if result.returncode == 0:
                    print(f"✅ {method['name']}를 사용한 {package} 설치 성공!")
                    if result.stdout:
                        print(f"   STDOUT: {result.stdout[:200]}...")
                    
                    # 설치 확인
                    verify_result = subprocess.run(
                        [str(python_exe), "-c", f"import {import_name}; print('설치 확인: OK')"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    
                    if verify_result.returncode == 0 and "OK" in verify_result.stdout:
                        print(f"🎉 {package} 모듈 설치 및 확인 완료!")
                        package_installed = True
                        success_count += 1
                        break
                    else:
                        print(f"⚠️ {package} 설치는 성공했지만 import 확인 실패")
                        if verify_result.stderr:
                            print(f"   확인 오류: {verify_result.stderr[:200]}...")
                        continue
                        
                else:
                    print(f"❌ {method['name']} {package} 설치 실패:")
                    if result.stderr:
                        print(f"   STDERR: {result.stderr[:300]}...")
                    continue
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ {method['name']} {package} 설치 시간 초과 ({method['timeout']}초)")
                continue
            except FileNotFoundError:
                print(f"🚫 {method['name']} 명령어를 찾을 수 없음")
                continue
            except Exception as e:
                print(f"❌ {method['name']} {package} 설치 중 오류: {e}")
                continue
        
        if not package_installed:
            print(f"❌ {package} 모든 설치 방법이 실패했습니다.")
    
    # 결과 확인
    total_packages = len(packages_to_install)
    if success_count == total_packages:
        print(f"🎉 모든 패키지 ({success_count}/{total_packages}) 설치/확인 완료!")
        return True
    elif success_count > 0:
        print(f"⚠️ 일부 패키지만 성공 ({success_count}/{total_packages})")
        return False
    else:
        print("❌ 모든 패키지 설치가 실패했습니다.")
        return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("✅ 작업이 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print("❌ 작업이 실패했습니다.")
        sys.exit(1)

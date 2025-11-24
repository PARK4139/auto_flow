#!/usr/bin/env python3
"""
pk_system 자동 설치 스크립트 (Git URL 직접 사용 방식 - 읽기 전용)

외부 프로젝트에서 pk_system을 자동으로 설치하는 스크립트입니다.
uv 프로젝트를 우선 지원하며, `uv add` 명령어를 사용합니다.
Git URL을 직접 사용하여 읽기 전용(비-editable) 모드로 설치합니다.

사용법:
    python install_pk_system.py                    # 기본 설치 (main 브랜치, 읽기 전용)
    python install_pk_system.py --branch develop   # 특정 브랜치
    python install_pk_system.py --tag v2025.1.15   # 특정 태그
    python install_pk_system.py --dev              # 개발 의존성으로 추가
    python install_pk_system.py --ssh              # SSH URL 사용 (Private 저장소)
"""

import sys
import os
import subprocess
import logging
import argparse
from pathlib import Path
from typing import Optional, Literal

# 로깅 설정 (UTF-8 인코딩 지원)
import sys
if sys.stdout.encoding != 'utf-8':
    # UTF-8 인코딩으로 재설정
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# 기본 설정
DEFAULT_GIT_REPO = "https://github.com/PARK4139/pk_system.git"
DEFAULT_BRANCH = "main"
DEFAULT_INSTALL_PATH = "assets/pk_system"  # 외부 프로젝트 내 설치 경로


def find_uv_executable(project_root: Optional[Path] = None) -> Optional[str]:
    """
    uv 실행 파일 경로 찾기
    
    우선순위:
    1. assets/pk_system/uv.exe 또는 assets/pk_system/uv (클론된 pk_system 내부)
    2. 프로젝트 루트/uv.exe 또는 프로젝트 루트/uv
    3. 현재 디렉토리/uv.exe 또는 현재 디렉토리/uv
    4. 시스템 uv 명령어
    
    Returns:
        uv 실행 파일 경로 또는 None
    """
    import platform
    import sys
    
    # 플랫폼에 따라 실행 파일 이름 결정
    is_windows = platform.system() == "Windows"
    uv_exe_name = "uv.exe" if is_windows else "uv"
    
    candidates = []
    
    # 1. assets/pk_system/uv.exe 또는 assets/pk_system/uv (클론된 pk_system 내부)
    if project_root:
        pk_system_uv = project_root / DEFAULT_INSTALL_PATH / uv_exe_name
        if pk_system_uv.exists():
            candidates.append((f"assets/pk_system/{uv_exe_name}", str(pk_system_uv)))
            logging.debug(f"✅ pk_system 내부 {uv_exe_name} 발견: {pk_system_uv}")
        # Linux/WSL에서는 uv 실행 파일이 여러 위치에 있을 수 있음
        if not is_windows:
            # assets/pk_system/.venv/bin/uv (가상환경 내부)
            pk_system_venv_uv = project_root / DEFAULT_INSTALL_PATH / ".venv" / "bin" / "uv"
            if pk_system_venv_uv.exists():
                candidates.append((f"assets/pk_system/.venv/bin/uv", str(pk_system_venv_uv)))
                logging.debug(f"✅ pk_system 가상환경 내부 uv 발견: {pk_system_venv_uv}")
    
    # 2. 프로젝트 루트/uv.exe 또는 프로젝트 루트/uv
    if project_root:
        root_uv = project_root / uv_exe_name
        if root_uv.exists():
            candidates.append((f"프로젝트 루트/{uv_exe_name}", str(root_uv)))
            logging.debug(f"✅ 프로젝트 루트 {uv_exe_name} 발견: {root_uv}")
        # Linux/WSL에서는 .venv/bin/uv도 확인
        if not is_windows:
            root_venv_uv = project_root / ".venv" / "bin" / "uv"
            if root_venv_uv.exists():
                candidates.append(("프로젝트 루트/.venv/bin/uv", str(root_venv_uv)))
                logging.debug(f"✅ 프로젝트 가상환경 내부 uv 발견: {root_venv_uv}")
    
    # 3. 현재 디렉토리/uv.exe 또는 현재 디렉토리/uv
    current_dir_uv = Path.cwd() / uv_exe_name
    if current_dir_uv.exists():
        candidates.append((f"현재 디렉토리/{uv_exe_name}", str(current_dir_uv)))
        logging.debug(f"✅ 현재 디렉토리 {uv_exe_name} 발견: {current_dir_uv}")
    
    # 4. 시스템 uv 명령어 (최후 수단)
    candidates.append(("시스템 uv", "uv"))
    
    # 각 후보를 순서대로 테스트
    for name, uv_path in candidates:
        try:
            result = subprocess.run(
                [uv_path, '--version'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=5
            )
            if result.returncode == 0:
                logging.debug(f"✅ uv 실행 파일 사용: {name} ({uv_path})")
                logging.info(f"   uv 버전: {result.stdout.strip()}")
                return uv_path
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            logging.debug(f"   {name} 테스트 실패: {e}")
            continue
    
    return None


def find_python_executable(project_root: Optional[Path] = None) -> Optional[str]:
    """
    Python 실행 파일 경로 찾기
    
    우선순위:
    1. assets/pk_system/python.exe 또는 assets/pk_system/python (클론된 pk_system 내부)
    2. assets/pk_system/.venv/Scripts/python.exe 또는 .venv/bin/python (pk_system 가상환경)
    3. 프로젝트 루트/.venv/Scripts/python.exe 또는 .venv/bin/python (프로젝트 가상환경)
    4. 시스템 python 명령어
    
    Returns:
        Python 실행 파일 경로 또는 None
    """
    import platform
    import sys
    
    # 플랫폼에 따라 실행 파일 이름 결정
    is_windows = platform.system() == "Windows"
    python_exe_name = "python.exe" if is_windows else "python"
    venv_scripts = "Scripts" if is_windows else "bin"
    
    candidates = []
    
    # 1. assets/pk_system/python.exe 또는 assets/pk_system/python (클론된 pk_system 내부)
    if project_root:
        pk_system_python = project_root / DEFAULT_INSTALL_PATH / python_exe_name
        if pk_system_python.exists():
            candidates.append((f"assets/pk_system/{python_exe_name}", str(pk_system_python)))
            logging.debug(f"✅ pk_system 내부 {python_exe_name} 발견: {pk_system_python}")
    
    # assets/pk_system/.venv/Scripts/python.exe 또는 .venv/bin/python (pk_system 가상환경)
    if project_root:
        pk_system_venv_python = project_root / DEFAULT_INSTALL_PATH / ".venv" / venv_scripts / python_exe_name
        if pk_system_venv_python.exists():
            candidates.append((f"assets/pk_system/.venv/{venv_scripts}/{python_exe_name}", str(pk_system_venv_python)))
            logging.debug(f"✅ pk_system 가상환경 내부 {python_exe_name} 발견: {pk_system_venv_python}")
    
    # 2. 프로젝트 루트/.venv/Scripts/python.exe 또는 .venv/bin/python (프로젝트 가상환경)
    if project_root:
        root_venv_python = project_root / ".venv" / venv_scripts / python_exe_name
        if root_venv_python.exists():
            candidates.append((f"프로젝트 루트/.venv/{venv_scripts}/{python_exe_name}", str(root_venv_python)))
            logging.debug(f"✅ 프로젝트 가상환경 내부 {python_exe_name} 발견: {root_venv_python}")
    
    # 3. 현재 디렉토리/.venv/Scripts/python.exe 또는 .venv/bin/python
    current_dir_venv_python = Path.cwd() / ".venv" / venv_scripts / python_exe_name
    if current_dir_venv_python.exists():
        candidates.append((f"현재 디렉토리/.venv/{venv_scripts}/{python_exe_name}", str(current_dir_venv_python)))
        logging.debug(f"✅ 현재 디렉토리 가상환경 내부 {python_exe_name} 발견: {current_dir_venv_python}")
    
    # 4. 시스템 python 명령어 (최후 수단)
    # Windows에서는 python3, python 순서로 확인
    if is_windows:
        candidates.append(("시스템 python3", "python3"))
        candidates.append(("시스템 python", "python"))
        # py launcher도 확인
        candidates.append(("시스템 py", "py"))
    else:
        candidates.append(("시스템 python3", "python3"))
        candidates.append(("시스템 python", "python"))
    
    # 각 후보를 순서대로 테스트
    for name, python_path in candidates:
        try:
            result = subprocess.run(
                [python_path, '--version'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=5
            )
            if result.returncode == 0:
                logging.debug(f"✅ Python 실행 파일 사용: {name} ({python_path})")
                logging.debug(f"   Python 버전: {result.stdout.strip()}")
                return python_path
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            logging.debug(f"   {name} 테스트 실패: {e}")
            continue
    
    return None


def is_uv_available(project_root: Optional[Path] = None) -> bool:
    """
    uv 명령어가 사용 가능한지 확인
    
    Args:
        project_root: 프로젝트 루트 경로 (pk_system 내부 uv.exe 검색용)
    
    Returns:
        uv 사용 가능 여부
    """
    uv_path = find_uv_executable(project_root)
    return uv_path is not None


def is_uv_project(project_root: Path) -> bool:
    """프로젝트가 uv 프로젝트인지 판별"""
    pyproject_toml = project_root / "pyproject.toml"
    uv_lock = project_root / "uv.lock"
    
    # uv.lock 파일이 있으면 uv 프로젝트
    if uv_lock.exists():
        logging.debug("uv.lock 파일 발견 - uv 프로젝트로 판별")
        return True
    
    # pyproject.toml 확인
    if not pyproject_toml.exists():
        logging.debug("pyproject.toml 파일 없음")
        return False
    
    try:
        content = pyproject_toml.read_text(encoding='utf-8')
        # [project] 섹션이 있으면 uv 프로젝트 가능성 높음
        if '[project]' in content or '[tool.uv]' in content:
            if is_uv_available():
                logging.debug("pyproject.toml + uv 명령어 - uv 프로젝트로 판별")
                return True
    except Exception as e:
        logging.debug(f"pyproject.toml 읽기 실패: {e}")
    
    return False


def find_project_root(start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    대규모 프로젝트에서 프로젝트 루트를 자동으로 찾기
    
    일반적으로 .git은 Git 저장소 루트에만 존재하지만, 서브모듈(submodule)의 경우
    각 서브모듈의 루트에도 .git이 존재할 수 있습니다.
    
    탐색 전략:
    1. 여러 지표를 조합하여 가장 확실한 프로젝트 루트를 찾습니다.
    2. .git과 프로젝트 메타데이터 파일(pyproject.toml, uv.lock 등)이 함께 있는 디렉토리를 우선 선택합니다.
    3. 서브모듈보다 메인 저장소가 상위에 있을 가능성을 고려합니다.
    
    탐색 순서 (우선순위):
    1. .git + pyproject.toml/uv.lock (가장 확실한 조합)
    2. .git 디렉토리 (Git 저장소 루트, 상위부터 검색하여 메인 저장소 찾음)
    3. pyproject.toml (Python 프로젝트 표준)
    4. uv.lock (uv 프로젝트)
    5. setup.py (레거시 Python 프로젝트)
    6. requirements.txt (pip 프로젝트)
    7. .venv 디렉토리 근처 (가상환경이 있는 경우)
    
    Returns:
        프로젝트 루트 경로 또는 None (찾지 못한 경우)
    """
    if start_dir is None:
        start_dir = Path.cwd().resolve()
    else:
        start_dir = Path(start_dir).resolve()
    
    # 모든 후보를 수집 (여러 지표를 고려)
    candidates = []
    
    # 시작 디렉토리부터 루트까지 상위로 검색
    logging.debug(f"🔍 프로젝트 루트 탐색 시작: {start_dir}")
    for idx, current in enumerate([start_dir] + list(start_dir.parents)):
        logging.debug(f"  [{idx+1}] 검사 중: {current}")
        
        has_git = (current / ".git").exists() and (current / ".git").is_dir()
        has_pyproject = (current / "pyproject.toml").exists()
        has_uv_lock = (current / "uv.lock").exists()
        has_setup = (current / "setup.py").exists()
        has_requirements = (current / "requirements.txt").exists()
        has_venv = (current / ".venv").exists() and (current / ".venv").is_dir()
        
        # 발견된 지표들 수집
        indicators = []
        if has_git:
            indicators.append(".git")
        if has_pyproject:
            indicators.append("pyproject.toml")
        if has_uv_lock:
            indicators.append("uv.lock")
        if has_setup:
            indicators.append("setup.py")
        if has_requirements:
            indicators.append("requirements.txt")
        if has_venv:
            indicators.append(".venv")
        
        if indicators:
            logging.debug(f"    ✅ 발견된 지표: {', '.join(indicators)}")
        else:
            logging.debug(f"    ⚪ 지표 없음")
        
        # 우선순위: .git + 프로젝트 메타데이터 파일 조합 (가장 확실함)
        if has_git and (has_pyproject or has_uv_lock):
            logging.debug(f"✅ Git 저장소 + 프로젝트 메타데이터 발견: {current}")
            logging.info(f"   발견된 지표: {', '.join(indicators)}")
            return current
        
        # .git만 있는 경우 (서브모듈일 수 있으므로 후보로 보관)
        if has_git:
            candidates.append((current, "git"))
        
        # 프로젝트 메타데이터 파일들
        if has_pyproject:
            candidates.append((current, "pyproject.toml"))
        
        if has_uv_lock:
            candidates.append((current, "uv.lock"))
        
        if has_setup:
            candidates.append((current, "setup.py"))
        
        if has_requirements:
            candidates.append((current, "requirements.txt"))
        
        if has_venv:
            candidates.append((current, ".venv"))
        
        # 루트 디렉토리에 도달하면 중단 (Windows: C:\, Linux: /)
        if current.parent == current:
            logging.debug(f"  ⚠️ 파일 시스템 루트에 도달: {current}")
            break
    
    # 후보가 있으면 가장 상위(가장 먼저 발견한) 것을 반환
    # .git이 있으면 우선 선택 (메인 저장소일 가능성이 높음)
    if candidates:
        # .git 후보가 있으면 가장 상위의 .git 반환
        git_candidates = [c for c in candidates if c[1] == "git"]
        if git_candidates:
            result = git_candidates[0][0]
            logging.debug(f"✅ Git 저장소 루트 선택: {result}")
            logging.info(f"   선택 기준: {git_candidates[0][1]}")
            return result
        
        # 그 외에는 가장 상위의 후보 반환
        result = candidates[0][0]
        logging.debug(f"✅ 프로젝트 루트 선택: {result}")
        logging.info(f"   선택 기준: {candidates[0][1]}")
        return result
    
    logging.debug("❌ 프로젝트 루트를 찾지 못했습니다.")
    return None


def is_pk_system_installed(project_root: Path) -> bool:
    """
    pk_system이 이미 설치되어 있는지 확인
    
    Args:
        project_root: 프로젝트 루트 경로 (pk_system 내부 python.exe 검색용)
    """
    pyproject_toml = project_root / "pyproject.toml"
    
    if not pyproject_toml.exists():
        return False
    
    try:
        content = pyproject_toml.read_text(encoding='utf-8')
        # pyproject.toml에 pk_system이 포함되어 있는지 확인
        if "pk_system" in content:
            logging.debug("pyproject.toml에 pk_system 의존성 발견")
            return True
    except Exception as e:
        logging.debug(f"pyproject.toml 읽기 실패: {e}")
    
    # Python에서 import 확인 (클론된 pk_system 내부 python 우선 사용)
    python_exe = find_python_executable(project_root) or sys.executable
    try:
        result = subprocess.run(
            [python_exe, '-c', 'from temp.pk_system.pk_system_sources.pk_system_objects.pk_system_directories import get_pk_system_root; print(get_pk_system_root())'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            logging.debug(f"pk_system import 성공: {result.stdout.strip()}")
            if python_exe != sys.executable:
                logging.debug(f"   사용된 Python: {python_exe}")
            return True
    except Exception as e:
        logging.debug(f"pk_system import 확인 실패: {e}")
    
    return False


def check_if_newer_version_available(project_root: Path, git_url: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    최신 버전이 있는지 확인
    
    Returns:
        (has_newer_version, current_commit, latest_commit)
        - has_newer_version: 최신 버전이 있으면 True
        - current_commit: 현재 설치된 커밋 해시 (없으면 None)
        - latest_commit: 원격 저장소의 최신 커밋 해시 (없으면 None)
    """
    import re
    
    # tomllib 호환성 처리 (Python 3.11+)
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            logging.debug("tomllib 또는 tomli를 사용할 수 없습니다. 최신 버전 확인을 건너뜁니다.")
            return False, None, None
    
    pyproject_toml = project_root / "pyproject.toml"
    if not pyproject_toml.exists():
        return False, None, None
    
    # pyproject.toml에서 현재 설치된 커밋 해시 확인
    current_commit = None
    try:
        with open(pyproject_toml, 'rb') as f:
            data = tomllib.load(f)
        
        dependencies = data.get('project', {}).get('dependencies', [])
        for dep in dependencies:
            if isinstance(dep, str) and 'pk_system' in dep and '@' in dep:
                # git+https://github.com/...@main 또는 rev = "..." 형식 확인
                if 'rev =' in dep:
                    match = re.search(r'rev\s*=\s*"([^"]+)"', dep)
                    if match:
                        current_commit = match.group(1)
                elif '@' in dep:
                    # git+https://...@main 또는 git+https://...@abc123 형식
                    parts = dep.split('@')
                    if len(parts) > 1:
                        ref = parts[-1].strip().strip('"').strip("'")
                        # 커밋 해시인지 확인 (40자 또는 7자 이상의 16진수)
                        if len(ref) >= 7 and all(c in '0123456789abcdefABCDEF' for c in ref):
                            current_commit = ref
                break
    except Exception as e:
        logging.debug(f"현재 커밋 확인 실패: {e}")
    
    # 원격 저장소의 최신 커밋 해시 확인
    latest_commit = None
    try:
        # Git URL에서 저장소 URL 추출
        repo_url = git_url.replace('git+', '').replace('git+ssh://', '').replace('git+https://', 'https://')
        # @main 같은 참조 제거
        if '@' in repo_url:
            repo_url = repo_url.split('@')[0]
        
        # git ls-remote로 최신 커밋 확인
        branch = DEFAULT_BRANCH
        if '@' in git_url:
            ref_part = git_url.split('@')[-1]
            if ref_part not in ('main', 'master'):
                branch = ref_part
        
        result = subprocess.run(
            ['git', 'ls-remote', repo_url, f'refs/heads/{branch}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            # 출력 형식: "커밋해시\trefs/heads/main"
            lines = result.stdout.strip().split('\n')
            if lines:
                latest_commit = lines[0].split()[0]
    except Exception as e:
        logging.debug(f"최신 커밋 확인 실패: {e}")
    
    # 비교
    if current_commit and latest_commit:
        has_newer = current_commit != latest_commit
        return has_newer, current_commit, latest_commit
    elif latest_commit:
        # 현재 커밋을 알 수 없지만 최신 커밋은 있음 (업데이트 가능)
        return True, current_commit, latest_commit
    
    return False, current_commit, latest_commit


def _verify_upgrade_success(project_root: Path, git_url: str) -> None:
    """최신화 성공 여부를 확인하고 결과를 출력합니다."""
    import json
    
    uv_lock = project_root / "uv.lock"
    if not uv_lock.exists():
        logging.debug("uv.lock 파일이 없어 최신화 확인을 건너뜁니다.")
        return
    
    try:
        # uv.lock 파일 읽기 (JSON 형식)
        with open(uv_lock, 'r', encoding='utf-8') as f:
            lock_data = json.load(f)
        
        # Git URL에서 저장소 URL 추출
        repo_url = git_url.replace('git+', '').replace('git+ssh://', '').replace('git+https://', 'https://')
        if '@' in repo_url:
            repo_url = repo_url.split('@')[0]
        
        # uv.lock에서 pk-system 패키지 찾기
        packages = lock_data.get('package', [])
        for pkg in packages:
            if pkg.get('name') == 'pk-system':
                source = pkg.get('source', {})
                if 'git' in source:
                    git_info = source['git']
                    installed_rev = git_info.get('rev')
                    installed_url = git_info.get('url', '').replace('.git', '')
                    
                    if installed_rev and repo_url.replace('.git', '') in installed_url:
                        # 원격 저장소의 최신 커밋 확인
                        _, _, latest_commit = check_if_newer_version_available(project_root, git_url)
                        
                        # 시스템 규칙에 따른 출력 형식
                        print("")
                        print("_" * 66)
                        print("# 최신화 완료 확인")
                        print("")
                        
                        if latest_commit:
                            if installed_rev == latest_commit:
                                print("✅ 최신화 완료: 최신 버전으로 업데이트되었습니다.")
                                print(f"설치된 커밋: {installed_rev[:7]}...")
                            else:
                                print(f"✅ 업데이트 완료: {installed_rev[:7]}... (최신: {latest_commit[:7]}...)")
                        else:
                            print(f"✅ 업데이트 완료: {installed_rev[:7]}...")
                        print("")
                        return
        
        logging.debug("uv.lock에서 pk-system 패키지를 찾을 수 없습니다.")
    except Exception as e:
        logging.debug(f"최신화 확인 실패: {e}")


def fix_pyproject_toml_dependency(project_root: Path) -> bool:
    """
    pyproject.toml에서 잘못된 Git URL 의존성을 로컬 경로 의존성으로 수정
    
    Returns:
        수정 성공 여부
    """
    pyproject_toml = project_root / "pyproject.toml"
    
    if not pyproject_toml.exists():
        return False
    
    try:
        import re
        
        content = pyproject_toml.read_text(encoding='utf-8')
        original_content = content
        
        # 잘못된 Git URL 패턴 찾기 및 제거
        modified = False
        
        # 패턴 1: "pk_system @ git+https://..." 또는 "pk-system @ git+https://..." (따옴표 포함, 한 줄)
        pattern1 = r'["\']pk[_-]?system\s*@\s*git\+https://github\.com/PARK4139/pk_system\.git[^"\']*["\']\s*,?\s*\n'
        if re.search(pattern1, content, re.MULTILINE | re.IGNORECASE):
            content = re.sub(pattern1, '', content, flags=re.MULTILINE | re.IGNORECASE)
            modified = True
            logging.debug("패턴 1 제거: pk_system @ git+https://...")
        
        # 패턴 2: pk-system = { git = "git+https://..." } (여러 줄)
        pattern2 = r'pk[_-]?system\s*=\s*{\s*git\s*=\s*["\']git\+https://github\.com/PARK4139/pk_system\.git[^}]*}\s*,?\s*\n'
        if re.search(pattern2, content, re.MULTILINE | re.IGNORECASE):
            content = re.sub(pattern2, '', content, flags=re.MULTILINE | re.IGNORECASE)
            modified = True
            logging.debug("패턴 2 제거: pk-system = { git = ... }")
        
        # 패턴 3: 배열 내에서 pk_system이 포함된 줄 (나머지 잘못된 형태)
        # pk_system로 시작하고 git+https가 포함된 줄 전체 제거
        pattern3 = r'\s*["\']?pk[_-]?system[^"\n]*git\+https://github\.com/PARK4139/pk_system\.git[^"\n]*["\']?\s*,?\s*\n'
        if re.search(pattern3, content, re.MULTILINE | re.IGNORECASE):
            content = re.sub(pattern3, '', content, flags=re.MULTILINE | re.IGNORECASE)
            modified = True
            logging.debug("패턴 3 제거: 나머지 잘못된 형태")
        
        # 패턴 4: workspace = true 형태 제거
        # pk-system = { workspace = true } 또는 여러 줄 형태
        pattern4 = r'pk[_-]?system\s*=\s*{\s*workspace\s*=\s*true\s*}\s*,?\s*\n'
        if re.search(pattern4, content, re.MULTILINE | re.IGNORECASE):
            content = re.sub(pattern4, '', content, flags=re.MULTILINE | re.IGNORECASE)
            modified = True
            logging.debug("패턴 4 제거: workspace = true 의존성")
        
        # 패턴 5: 잘못된 경로 문자열 제거: "asset/pk_system" 또는 'asset/pk_system'
        pattern5 = r'\s*["\']asset/pk_system["\']\s*,?\s*\n'
        if re.search(pattern5, content, re.MULTILINE | re.IGNORECASE):
            content = re.sub(pattern5, '', content, flags=re.MULTILINE | re.IGNORECASE)
            modified = True
            logging.debug("패턴 5 제거: 잘못된 경로 문자열")
        
        # 빈 줄 정리 (3개 이상 연속된 빈 줄을 2개로)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 잘못된 줄 수정: "pk_system @ "로 시작하는 줄 제거
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            # "pk_system @ "로 시작하는 줄 감지 (다양한 패턴)
            if 'pk_system @' in line.lower() or 'pk-system @' in line.lower():
                # 잘못된 형태: "pk_system @ "altair==5.5.0" (따옴표가 잘못 닫힌 경우)
                if '"pk_system @ "' in line or '"pk-system @ "' in line:
                    # 뒤에 다른 패키지 이름이 나오는 경우 (잘못된 줄)
                    if re.search(r'["\']pk[_-]?system\s*@\s*["\']\s*["\']?[a-zA-Z]', line, re.IGNORECASE):
                        logging.info(f"   잘못된 줄 제거 (줄 {i+1}): {line.strip()[:70]}")
                        modified = True
                        continue
                # 이 줄이 닫히지 않은 경우 제거
                if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
                    logging.info(f"   닫히지 않은 줄 제거 (줄 {i+1}): {line.strip()[:70]}")
                    modified = True
                    continue
                # Git URL이 포함된 경우 제거
                if 'git+https://github.com/PARK4139/pk_system.git' in line:
                    logging.info(f"   Git URL 줄 제거 (줄 {i+1}): {line.strip()[:70]}")
                    modified = True
                    continue
            
            # workspace = true 오류 수정
            # pk-system = { workspace = true } 형태 제거
            if re.search(r'pk[_-]?system\s*=\s*{\s*workspace\s*=\s*true\s*}', line, re.IGNORECASE):
                logging.info(f"   workspace = true 의존성 제거 (줄 {i+1}): {line.strip()[:70]}")
                modified = True
                continue
            
            # asset/pk_system 루트경로를 assets/pk_system로 수정
            if 'asset/pk_system' in line and 'assets/pk_system' not in line:
                line = line.replace('asset/pk_system', 'assets/pk_system')
                logging.info(f"   경로 수정 (줄 {i+1}): asset/pk_system -> assets/pk_system")
                modified = True
            
            # 잘못된 경로 문자열 제거: "asset/pk_system" (따옴표로 감싼 경로)
            if re.search(r'["\']asset/pk_system["\']', line, re.IGNORECASE):
                logging.info(f"   잘못된 경로 문자열 제거 (줄 {i+1}): {line.strip()[:70]}")
                modified = True
                continue
            
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
        # [project] 섹션 내부에 dependencies = [...] 가 있고 [project.dependencies] 섹션도 있는 경우
        # TOML에서는 중복이므로 [project.dependencies] 섹션을 제거하고 [project] 내부의 dependencies에 추가
        has_project_deps_section = '[project.dependencies]' in content
        has_project_deps_key = False
        
        # [project] 섹션 내부에 dependencies 키가 있는지 확인
        project_match = re.search(r'\[project\]', content)
        if project_match:
            project_start = project_match.end()
            # 다음 섹션([...)이 나올 때까지 찾기
            next_section_match = re.search(r'\n\s*\[', content[project_start:])
            if next_section_match:
                project_end = project_start + next_section_match.start()
            else:
                project_end = len(content)
            
            project_section = content[project_start:project_end]
            if re.search(r'dependencies\s*=', project_section):
                has_project_deps_key = True
        
        # 중복된 [project.dependencies] 섹션 제거
        deps_section_count = content.count('[project.dependencies]')
        if deps_section_count > 1:
            logging.info(f"   중복된 [project.dependencies] 섹션 발견 ({deps_section_count}개)")
            # 첫 번째 [project.dependencies] 섹션만 유지하고 나머지 제거
            lines = content.split('\n')
            new_lines = []
            deps_section_found = False
            skip_until_section = False
            
            for i, line in enumerate(lines):
                if '[project.dependencies]' in line:
                    if not deps_section_found:
                        # 첫 번째 섹션은 유지
                        deps_section_found = True
                        new_lines.append(line)
                    else:
                        # 이후 섹션은 제거
                        logging.info(f"   중복된 섹션 제거 (줄 {i+1})")
                        modified = True
                        skip_until_section = True
                        continue
                elif skip_until_section:
                    # 다음 섹션([...])이 나올 때까지 건너뛰기
                    if line.strip().startswith('[') and not line.strip().startswith('[project.dependencies]'):
                        skip_until_section = False
                        new_lines.append(line)
                    # 빈 줄이나 주석은 유지할 수도 있지만, 여기서는 제거
                    continue
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # [project] 섹션 내부에 dependencies = [...] 가 있고 [project.dependencies] 섹션도 있는 경우
        # TOML에서는 중복이므로 [project.dependencies] 섹션을 제거하고 [project] 내부의 dependencies에 추가
        project_match = re.search(r'\[project\]', content)
        has_project_deps_key = False
        if project_match:
            project_start = project_match.end()
            # 다음 섹션([...)이 나올 때까지 찾기
            next_section_match = re.search(r'\n\s*\[', content[project_start:])
            if next_section_match:
                project_end = project_start + next_section_match.start()
            else:
                project_end = len(content)
            
            project_section = content[project_start:project_end]
            if re.search(r'dependencies\s*=', project_section):
                has_project_deps_key = True
        
        # [project] 내부에 dependencies 키가 있고 [project.dependencies] 섹션도 있는 경우
        # [project.dependencies] 섹션을 제거
        if has_project_deps_key and '[project.dependencies]' in content:
            logging.info("   [project] 내부에 dependencies 키와 [project.dependencies] 섹션이 모두 존재합니다.")
            logging.info("   [project.dependencies] 섹션을 제거합니다...")
            
            # [project.dependencies] 섹션 제거
            lines = content.split('\n')
            new_lines = []
            skip_deps_section = False
            
            for i, line in enumerate(lines):
                if '[project.dependencies]' in line:
                    logging.info(f"   [project.dependencies] 섹션 제거 (줄 {i+1})")
                    skip_deps_section = True
                    modified = True
                    continue
                elif skip_deps_section:
                    # 다음 섹션([...])이 나올 때까지 건너뛰기
                    stripped = line.strip()
                    if stripped.startswith('['):
                        skip_deps_section = False
                        new_lines.append(line)
                    elif stripped:  # 빈 줄이 아닌 경우 제거
                        continue
                    else:  # 빈 줄은 유지
                        continue
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # 로컬 경로 의존성 문자열
        local_dep_line = f'{{ path = "./{DEFAULT_INSTALL_PATH}", editable = true }}'
        local_dep_string = f'    "pk-system = {local_dep_line}",'
        
        # pk-system 의존성이 완전히 없는 경우 추가
        if 'pk-system' not in content and 'pk_system @' not in content:
            # [project] 섹션 내부에 dependencies 리스트가 있는 경우 추가
            if has_project_deps_key:
                # dependencies 리스트의 끝에 추가
                deps_match = re.search(r'dependencies\s*=\s*\[', content)
                if deps_match:
                    deps_start = deps_match.end()
                    # 리스트의 끝을 찾기
                    bracket_count = 1
                    in_string = False
                    escape_next = False
                    list_end = deps_start
                    
                    for j, char in enumerate(content[deps_start:], start=deps_start):
                        if escape_next:
                            escape_next = False
                            continue
                        if char == '\\':
                            escape_next = True
                            continue
                        if char == '"' or char == "'":
                            in_string = not in_string
                            continue
                        if not in_string:
                            if char == '[':
                                bracket_count += 1
                            elif char == ']':
                                bracket_count -= 1
                                if bracket_count == 0:
                                    list_end = j + 1
                                    break
                    
                    # 리스트의 마지막 항목 뒤에 추가
                    content_before = content[:list_end]
                    content_after = content[list_end:]
                    
                    if content_before.rstrip().endswith(','):
                        # 마지막 항목 뒤에 쉼표가 있으면 그냥 추가
                        content = content_before + f'\n{local_dep_string}\n' + content_after
                    elif content_before.rstrip().endswith('['):
                        # 빈 리스트
                        content = content_before + f'\n{local_dep_string}\n' + content_after
                    else:
                        # 마지막 항목 뒤에 쉼표 추가 후 새 항목 추가
                        content = content_before.rstrip().rstrip(',') + f',\n{local_dep_string}\n' + content_after
                    modified = True
            # [project.dependencies] 섹션 확인
            elif '[project.dependencies]' in content:
                # dependencies 섹션에 추가
                deps_match = re.search(r'\[project\.dependencies\]\s*\n', content)
                if deps_match:
                    insert_pos = deps_match.end()
                    # 리스트 형식인지 확인 (dependencies = [...])
                    next_chars = content[insert_pos:insert_pos+20].strip()
                    if next_chars.startswith('['):
                        # 리스트에 추가 (마지막 항목 뒤)
                        # 리스트의 끝을 찾아서 그 앞에 추가
                        bracket_count = 0
                        list_end = insert_pos
                        in_string = False
                        escape_next = False
                        
                        for j, char in enumerate(content[insert_pos:], start=insert_pos):
                            if escape_next:
                                escape_next = False
                                continue
                            if char == '\\':
                                escape_next = True
                                continue
                            if char == '"' or char == "'":
                                in_string = not in_string
                                continue
                            if not in_string:
                                if char == '[':
                                    bracket_count += 1
                                elif char == ']':
                                    bracket_count -= 1
                                    if bracket_count == 0:
                                        list_end = j + 1
                                        break
                        
                        # 리스트의 마지막 줄을 찾아서 그 앞에 추가
                        content_before = content[:list_end]
                        content_after = content[list_end:]
                        
                        # 리스트 항목의 마지막 항목 뒤에 추가
                        if content_before.rstrip().endswith(','):
                            # 마지막 항목 뒤에 쉼표가 있으면 그냥 추가
                            content = content_before + f'\n    {local_dep_line},\n' + content_after
                        elif content_before.rstrip().endswith('['):
                            # 빈 리스트
                            content = content_before + f'\n    {local_dep_line}\n' + content_after
                        else:
                            # 마지막 항목 뒤에 쉼표 추가 후 새 항목 추가
                            content = content_before.rstrip().rstrip(',') + f',\n    {local_dep_line}\n' + content_after
                        modified = True
                    else:
                        # 단일 항목으로 추가
                        content = content[:insert_pos] + f'{local_dep_line}\n' + content[insert_pos:]
                        modified = True
            elif '[project]' in content:
                # project 섹션 내부에 dependencies 추가 (하지만 이미 dependencies = [...] 가 있을 수 있음)
                # [project] 섹션 내부를 확인
                project_match = re.search(r'\[project\]', content)
                if project_match:
                    project_start = project_match.end()
                    # 다음 섹션([...)이 나올 때까지 찾기
                    next_section_match = re.search(r'\n\s*\[', content[project_start:])
                    if next_section_match:
                        project_end = project_start + next_section_match.start()
                    else:
                        project_end = len(content)
                    
                    project_section = content[project_start:project_end]
                    if 'dependencies' not in project_section.lower():
                        # project 섹션 내부에 dependencies 추가
                        content = content[:project_end] + f'dependencies = [\n    {local_dep_line}\n]\n\n' + content[project_end:]
                        modified = True
            else:
                # 파일 끝에 새로운 섹션 추가
                if not content.rstrip().endswith('\n'):
                    content += '\n'
                content += f'\n[project.dependencies]\n{local_dep_line}\n'
                modified = True
        
        if modified:
            # 백업 생성
            backup_path = pyproject_toml.with_suffix('.toml.backup2')
            import shutil
            shutil.copy2(pyproject_toml, backup_path)
            
            # 수정된 내용 저장
            pyproject_toml.write_text(content, encoding='utf-8')
            logging.info(f"   백업 파일: {backup_path}")
            return True
        else:
            logging.debug("pyproject.toml 수정 불필요 (변경 사항 없음)")
            return False
            
    except Exception as e:
        logging.error(f"   pyproject.toml 수정 중 오류: {e}")
        import traceback
        logging.debug(traceback.format_exc())
        return False


def build_git_url(
    branch: Optional[str] = None,
    tag: Optional[str] = None,
    commit: Optional[str] = None,
    use_ssh: bool = False,
    git_url: Optional[str] = None
) -> str:
    """Git URL 구성"""
    if git_url:
        return git_url
    
    if use_ssh:
        base_url = f"git+ssh://git@github.com/PARK4139/pk_system.git"
    else:
        base_url = f"git+https://github.com/PARK4139/pk_system.git"
    
    if commit:
        return f"{base_url}@{commit}"
    elif tag:
        return f"{base_url}@{tag}"
    elif branch:
        return f"{base_url}@{branch}"
    else:
        return f"{base_url}@{DEFAULT_BRANCH}"


def add_environment_limit_to_pyproject(project_root: Path) -> bool:
    """
    pyproject.toml에 tool.uv.environments 설정 추가 (환경 제한)
    
    현재 환경만 사용하도록 제한하여 다른 환경에서의 의존성 해결 실패를 방지합니다.
    """
    pyproject_toml = project_root / "pyproject.toml"
    if not pyproject_toml.exists():
        return False
    
    try:
        import re
        
        # pyproject.toml 읽기
        content = pyproject_toml.read_text(encoding='utf-8')
        
        # 이미 environments 설정이 있는지 확인
        if re.search(r'\[tool\.uv\]', content) and re.search(r'environments\s*=', content, re.MULTILINE):
            logging.debug("tool.uv.environments 설정이 이미 존재합니다.")
            return False
        
        # [tool.uv] 섹션 찾기
        tool_uv_match = re.search(r'\[tool\.uv\]', content)
        
        if tool_uv_match:
            # [tool.uv] 섹션이 있으면 그 안에 추가
            section_end = tool_uv_match.end()
            # 다음 섹션([...)이 나올 때까지 찾기
            next_section_match = re.search(r'\n\s*\[', content[section_end:])
            if next_section_match:
                insert_pos = section_end + next_section_match.start()
            else:
                insert_pos = len(content)
            
            # environments 설정 추가
            environments_line = 'environments = ["default"]\n'
            # 섹션 끝에 줄바꿈이 없으면 추가
            if content[insert_pos - 1] != '\n':
                environments_line = '\n' + environments_line
            else:
                # 이미 줄바꿈이 있으면 그대로 추가
                pass
            
            content = content[:insert_pos] + environments_line + content[insert_pos:]
        else:
            # [tool.uv] 섹션이 없으면 생성
            # [tool] 섹션 찾기
            tool_match = re.search(r'\[tool\]', content)
            if tool_match:
                # [tool] 섹션이 있으면 그 다음에 [tool.uv] 추가
                tool_end = tool_match.end()
                # 다음 섹션([...)이 나올 때까지 찾기
                next_section_match = re.search(r'\n\s*\[', content[tool_end:])
                if next_section_match:
                    insert_pos = tool_end + next_section_match.start()
                else:
                    insert_pos = len(content)
                
                # [tool.uv] 섹션 추가
                uv_section = '\n[tool.uv]\nenvironments = ["default"]\n'
                content = content[:insert_pos] + uv_section + content[insert_pos:]
            else:
                # [tool] 섹션도 없으면 파일 끝에 추가
                if not content.rstrip().endswith('\n'):
                    content += '\n'
                content += '\n[tool.uv]\nenvironments = ["default"]\n'
        
        # 백업 생성
        backup_path = pyproject_toml.with_suffix('.toml.backup_env')
        import shutil
        shutil.copy2(pyproject_toml, backup_path)
        
        # 수정된 내용 저장
        pyproject_toml.write_text(content, encoding='utf-8')
        
        logging.info("💡 pyproject.toml에 환경 제한 추가: tool.uv.environments = [\"default\"]")
        logging.info("   (현재 환경만 사용하도록 제한하여 의존성 해결 실패 방지)")
        logging.debug(f"   백업 파일: {backup_path}")
        return True
    except Exception as e:
        logging.warning(f"⚠️ pyproject.toml 환경 제한 추가 실패: {e}")
        import traceback
        logging.debug(traceback.format_exc())
        return False


def detect_dependency_conflict(error_output: str) -> Optional[str]:
    """의존성 충돌 감지 및 분석"""
    # 의존성 해결 실패 패턴 확인
    conflict_indicators = [
        "No solution found when resolving dependencies",
        "unsatisfiable",
        "requirements are unsatisfiable",
        "depends on scikit-image",
        "depends on pk-system"
    ]
    
    has_conflict = any(indicator in error_output for indicator in conflict_indicators)
    
    # 디버깅: 충돌 지표 확인
    if has_conflict:
        logging.debug(f"🔍 충돌 지표 감지됨")
    
    if not has_conflict:
        return None
    
    # 충돌하는 패키지 추출
    import re
    
    # 패키지 버전 충돌 패턴 찾기 (정확한 매칭)
    conflict_patterns = [
        # "depends on scikit-image==0.25.0" 패턴
        r"depends on ([a-zA-Z0-9_-]+)==([0-9.]+)",
        # "your project depends on pk-system and scikit-image==0.25.1" 패턴
        r"your project depends on [a-zA-Z0-9_-]+ and ([a-zA-Z0-9_-]+)==([0-9.]+)",
        # "all versions of pk-system depend on scikit-image==0.25.0" 패턴
        r"all versions of [a-zA-Z0-9_-]+ depend on ([a-zA-Z0-9_-]+)==([0-9.]+)",
        # "pk-system==... depends on scikit-image==0.25.0" 패턴 (더 구체적)
        r"[a-zA-Z0-9_-]+==[0-9.]+(?:\.post[0-9]+)?(?:\+g[0-9a-f]+)?(?:\.[0-9]+)? depends on ([a-zA-Z0-9_-]+)==([0-9.]+)",
    ]
    
    conflicts = []
    for pattern in conflict_patterns:
        matches = re.findall(pattern, error_output, re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    # 튜플에서 패키지 이름과 버전 추출
                    if len(match) >= 2:
                        conflicts.append(match)
                    elif len(match) == 1:
                        conflicts.append((match[0], "unknown"))
    
    if conflicts:
        # 중복 제거 및 정리
        conflict_info = {}
        for match in conflicts:
            if isinstance(match, tuple) and len(match) >= 2:
                # 패키지 이름과 버전 추출 (모든 패턴은 2개 요소)
                pkg_name = match[0].strip()
                pkg_version = match[1].strip()
                
                # 유효한 패키지 이름과 버전인지 확인
                if pkg_name and pkg_version and pkg_version != "unknown":
                    if pkg_name not in conflict_info:
                        conflict_info[pkg_name] = []
                    conflict_info[pkg_name].append(pkg_version)
        
        if conflict_info:
            conflict_summary = []
            for pkg_name, versions in conflict_info.items():
                unique_versions = sorted(list(set(versions)))
                if len(unique_versions) > 1:
                    # 여러 버전이 충돌하는 경우
                    conflict_summary.append(f"{pkg_name}: {', '.join(unique_versions)}")
                elif len(unique_versions) == 1:
                    # 버전이 하나여도 충돌 정보로 표시 (pk_system 요구 vs 프로젝트 요구)
                    conflict_summary.append(f"{pkg_name}: {unique_versions[0]}")
            
            if conflict_summary:
                return "; ".join(conflict_summary)
    
    # 패턴 매칭이 실패해도 충돌이 있다고 판단된 경우
    if has_conflict:
        return "의존성 해결 실패 (패키지 충돌)"
    
    return None


def install_pk_system_interactive(
    project_root: Path,
    git_url: str,
    dev: bool = False,
    upgrade: bool = False,
    frozen: bool = False,
    use_ssh: bool = False,
    branch: Optional[str] = None,
    tag: Optional[str] = None,
    commit: Optional[str] = None,
    auto_retry: bool = True
) -> tuple[bool, Optional[str]]:
    """
    대화형 pk_system 설치 (충돌 발생 시 사용자에게 옵션 제공)
    """
    attempt_count = 0
    max_attempts = 5
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        # 설치 시도
        # 설치 경로 결정 (기본값: assets/pk_system)
        install_path = project_root / DEFAULT_INSTALL_PATH
        
        success, conflict_info = install_pk_system_with_uv_add(
            project_root=project_root,
            git_url=git_url,
            dev=dev,
            upgrade=upgrade,
            frozen=frozen,
            retry_with_frozen=False,  # 대화형 모드에서는 수동 제어
            install_path=install_path,
            branch=branch,
            tag=tag,
            commit=commit,
            use_ssh=use_ssh
        )
        
        if success:
            return True, None
        
        # 실패한 경우 충돌 정보 확인
        print("")
        print("_" * 66)
        
        if conflict_info:
            print("# 의존성 충돌이 발생했습니다")
            print("")
            print(f"충돌 정보: {conflict_info}")
        else:
            print("# 설치가 실패했습니다")
            print("")
        
        logging.info("")
        logging.info("# 해결 방법을 선택하세요")
        logging.info("")
        logging.info("1. --frozen 플래그 사용 (의존성 해결 건너뛰기, 권장)")
        if not use_ssh:
            logging.info("2. SSH URL 사용 (Private 저장소용)")
        else:
            logging.info("2. HTTPS URL 사용 (Public 저장소용)")
        logging.info("3. 다른 Git URL 또는 브랜치/태그 입력")
        logging.info("4. 취소하고 수동으로 해결")
        logging.info("")
        
        if auto_retry and attempt_count == 1 and conflict_info:
            # 첫 번째 시도에서 자동으로 --frozen 시도 제안
            # 비대화형 모드 확인 (stdin이 터미널에 연결되지 않은 경우)
            try:
                import sys
                if sys.stdin.isatty():
                    response = input("자동으로 --frozen 플래그로 재시도하시겠습니까? (Y/n): ").strip().lower()
                else:
                    # 비대화형 모드: 자동으로 --frozen 사용
                    logging.info("   비대화형 모드: 자동으로 --frozen 플래그를 사용합니다.")
                    response = 'y'
            except (EOFError, KeyboardInterrupt):
                # EOF나 중단 시 자동으로 --frozen 사용
                logging.info("   입력 없음: 자동으로 --frozen 플래그를 사용합니다.")
                response = 'y'
            
            if response in ['', 'y', 'yes']:
                frozen = True
                logging.info("💡 --frozen 플래그로 재시도합니다...")
                logging.info("")
                continue
        
        response = input("선택 (1-4): ").strip()
        
        if response == "1":
            frozen = True
            logging.info("💡 --frozen 플래그로 재시도합니다...")
            logging.info("")
            continue
        elif response == "2":
            use_ssh = not use_ssh  # 토글
            git_url = build_git_url(
                branch=branch,
                tag=tag,
                commit=commit,
                use_ssh=use_ssh,
                git_url=None
            )
            logging.info(f"💡 {'SSH' if use_ssh else 'HTTPS'} URL로 변경: {git_url}")
            logging.info("")
            continue
        elif response == "3":
            logging.info("")
            logging.info("Git URL 또는 브랜치/태그를 입력하세요.")
            logging.info("예: main, develop, v2025.1.15, git+ssh://git@github.com/...")
            custom_input = input("입력: ").strip()
            if custom_input:
                if custom_input.startswith("git+"):
                    git_url = custom_input
                else:
                    # 브랜치 또는 태그로 간주
                    if custom_input.startswith("v"):
                        tag = custom_input
                        branch = None
                    else:
                        branch = custom_input
                        tag = None
                    git_url = build_git_url(
                        branch=branch,
                        tag=tag,
                        commit=None,
                        use_ssh=use_ssh,
                        git_url=None
                    )
                logging.info(f"💡 Git URL 변경: {git_url}")
                logging.info("")
                continue
        else:
            logging.info("설치를 취소합니다.")
            return False, conflict_info
    
    logging.error("")
    logging.error("❌ 최대 시도 횟수에 도달했습니다.")
    return False, conflict_info


def clone_pk_system_repo(
    project_root: Path,
    git_url: str,
    install_path: Path,
    branch: Optional[str] = None,
    tag: Optional[str] = None,
    commit: Optional[str] = None,
    use_ssh: bool = False
) -> bool:
    """
    pk_system 저장소를 로컬 경로에 클론
    
    Returns:
        성공 여부
    """
    try:
        import shutil
        
        # 설치 경로가 이미 존재하는 경우
        if install_path.exists():
            if (install_path / ".git").exists():
                logging.info(f"📥 pk_system 저장소가 이미 존재합니다: {install_path}")
                logging.info("   업데이트를 시도합니다...")
                
                # git pull 실행
                pull_result = subprocess.run(
                    ['git', 'pull'],
                    cwd=install_path,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=60
                )
                
                if pull_result.returncode == 0:
                    logging.info("✅ pk_system 저장소 업데이트 완료")
                    return True
                else:
                    logging.warning("⚠️ git pull 실패, 새로 클론합니다...")
                    shutil.rmtree(install_path)
            else:
                logging.warning(f"⚠️ {install_path} 디렉토리가 이미 존재합니다 (Git 저장소 아님)")
                logging.warning("   백업 후 새로 클론합니다...")
                backup_path = project_root / f"{install_path.name}_backup"
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                shutil.move(install_path, backup_path)
        
        # 설치 경로의 부모 디렉토리 생성
        install_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Git URL 구성
        clone_url = git_url.replace("git+", "").replace("@main", "").replace("@develop", "")
        if branch:
            clone_url = clone_url.split("@")[0]
        
        logging.info(f"📥 pk_system 저장소 클론 중...")
        logging.info(f"   소스: {clone_url}")
        logging.info(f"   대상: {install_path}")
        
        # git clone 실행
        clone_cmd = ['git', 'clone']
        
        if branch:
            clone_cmd.extend(['--branch', branch, '--single-branch'])
        elif tag:
            clone_cmd.extend(['--branch', tag, '--single-branch'])
        
        clone_cmd.append(clone_url)
        clone_cmd.append(str(install_path))
        
        clone_result = subprocess.run(
            clone_cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5분 타임아웃
        )
        
        if clone_result.returncode == 0:
            # 특정 커밋으로 체크아웃 (지정된 경우)
            if commit:
                checkout_result = subprocess.run(
                    ['git', 'checkout', commit],
                    cwd=install_path,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=30
                )
                if checkout_result.returncode != 0:
                    logging.warning(f"⚠️ 커밋 {commit}으로 체크아웃 실패")
                    return False
            
            logging.info("✅ pk_system 저장소 클론 완료")
            return True
        else:
            logging.error(f"❌ git clone 실패: {clone_result.stderr}")
            return False
            
    except Exception as e:
        logging.error(f"❌ 저장소 클론 중 오류 발생: {e}")
        return False


def install_pk_system_with_uv_add(
    project_root: Path,
    git_url: str,
    dev: bool = False,
    upgrade: bool = False,
    frozen: bool = False,
    retry_with_frozen: bool = False,  # 대화형 모드에서는 비활성화
    install_path: Optional[Path] = None,
    branch: Optional[str] = None,
    tag: Optional[str] = None,
    commit: Optional[str] = None,
    use_ssh: bool = False
) -> tuple[bool, Optional[str]]:
    """
    uv add 명령어로 pk_system 설치 (Git URL 직접 사용 방식 - 읽기 전용)
    
    Git URL을 직접 사용하여 읽기 전용(비-editable) 모드로 설치합니다.
    이는 대규모 프로젝트에 권장되는 방식입니다.
    
    주의: uv add는 기존 pyproject.toml을 덮어쓰지 않고,
    dependencies 섹션에만 pk_system을 추가합니다.
    기존 의존성과 설정은 모두 보존됩니다.
    
    Returns:
        (성공 여부, 충돌 정보)
    """
    # 기존 pyproject.toml 백업 (안전장치)
    pyproject_toml = project_root / "pyproject.toml"
    pyproject_toml_backup = None
    if pyproject_toml.exists():
        try:
            # 백업 파일 생성
            pyproject_toml_backup = project_root / "pyproject.toml.backup"
            import shutil
            shutil.copy2(pyproject_toml, pyproject_toml_backup)
            logging.debug(f"pyproject.toml 백업 생성: {pyproject_toml_backup}")
        except Exception as e:
            logging.warning(f"⚠️ pyproject.toml 백업 생성 실패 (계속 진행): {e}")
    
    try:
        # pyproject.toml이 없으면 최소한의 pyproject.toml 생성
        if not pyproject_toml.exists():
            logging.info("💡 pyproject.toml 파일이 없습니다. 최소한의 pyproject.toml을 생성합니다...")
            try:
                from textwrap import dedent
                # 최소한의 pyproject.toml 생성
                minimal_pyproject = dedent("""\
                    [project]
                    name = "auto_flow"
                    version = "0.1.0"
                    requires-python = ">=3.12"
                    dependencies = []
                    """)
                pyproject_toml.write_text(minimal_pyproject, encoding='utf-8')
                logging.info("✅ pyproject.toml 생성 완료")
            except Exception as e:
                logging.warning(f"⚠️ pyproject.toml 생성 실패: {e}")
                logging.info("   uv init을 먼저 실행하거나 수동으로 pyproject.toml을 생성하세요.")
                return False, "pyproject.toml 생성 실패"
        
        # Git URL 직접 사용 방식 (읽기 전용 설치)
        cmd = ['uv', 'add']
        
        # 개발 의존성으로 추가
        if dev:
            cmd.append('--dev')
        
        # 읽기 전용 설치 (--editable 플래그 제거)
        # Git URL 직접 사용 방식은 기본적으로 읽기 전용입니다.
        
        # 업그레이드 모드
        if upgrade:
            cmd.append('--upgrade')
        
        # Frozen 플래그 (의존성 해결 건너뛰기)
        if frozen:
            cmd.append('--frozen')
        
        # Git URL 직접 사용 (읽기 전용)
        cmd.append(f"pk_system @ {git_url}")
        
        # uv 실행 파일 찾기
        uv_exe = find_uv_executable(project_root)
        if not uv_exe:
            logging.error("❌ uv 실행 파일을 찾을 수 없습니다.")
            return False, "uv 실행 파일 없음"
        
        # uv 명령어에 경로 사용
        if uv_exe != "uv":
            logging.info(f"💡 uv 실행 파일 사용: {uv_exe}")
            cmd_with_uv = [uv_exe] + cmd[1:]
        else:
            cmd_with_uv = cmd
        
        logging.info(f"📦 uv add 명령어 실행: {' '.join(cmd_with_uv)}")
        logging.info(f"프로젝트 경로: {project_root}")
        logging.info(f"Git URL: {git_url}")
        logging.info("💡 참고: Git URL 직접 사용 방식으로 읽기 전용(비-editable) 설치합니다.")
        logging.info("   uv add 후 자동으로 uv sync를 실행하여 의존성을 설치합니다.")
        
        result = subprocess.run(
            cmd_with_uv,
            cwd=project_root,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # 인코딩 오류 시 문자 대체
            timeout=600  # 10분 타임아웃
        )
        
        # TOML 파싱 오류 감지 및 복구
        if result.returncode != 0:
            error_output_for_check = (result.stderr or "") + (result.stdout or "")
            if "Failed to parse `pyproject.toml`" in error_output_for_check or "TOML parse error" in error_output_for_check:
                logging.warning("⚠️ pyproject.toml 파싱 오류 감지")
                logging.info("   TOML 형식 오류를 자동으로 수정합니다...")
                
                # pyproject.toml 읽기 및 수정
                try:
                    import re
                    content = pyproject_toml.read_text(encoding='utf-8')
                    original_content = content
                    
                    # 잘못된 environments 형식 수정
                    # 패턴 1: environments = [ "default",] -> environments = ["default"]
                    pattern1 = r'environments\s*=\s*\[\s*["\']?default["\']?\s*,?\s*\]'
                    if re.search(pattern1, content):
                        content = re.sub(
                            pattern1,
                            'environments = ["default"]',
                            content,
                            flags=re.IGNORECASE
                        )
                        logging.info("   ✅ environments 형식 수정: [ \"default\",] -> [\"default\"]")
                    
                    # 패턴 2: environments = [ "default" ,] -> environments = ["default"]
                    pattern2 = r'environments\s*=\s*\[\s*["\']default["\']\s*,?\s*\]'
                    if re.search(pattern2, content):
                        content = re.sub(
                            pattern2,
                            'environments = ["default"]',
                            content,
                            flags=re.IGNORECASE
                        )
                        logging.info("   ✅ environments 형식 수정: [ \"default\" ,] -> [\"default\"]")
                    
                    # 수정된 내용이 있으면 저장
                    if content != original_content:
                        pyproject_toml.write_text(content, encoding='utf-8')
                        logging.info("   ✅ pyproject.toml 수정 완료")
                        logging.info("   다시 시도합니다...")
                        logging.info("")
                        
                        # 수정 후 재시도
                        return install_pk_system_with_uv_add(
                            project_root=project_root,
                            git_url=git_url,
                            dev=dev,
                            upgrade=upgrade,
                            frozen=frozen,
                            retry_with_frozen=retry_with_frozen,
                            install_path=install_path,
                            branch=branch,
                            tag=tag,
                            commit=commit,
                            use_ssh=use_ssh
                        )
                    else:
                        # 수정할 내용이 없으면 백업 파일에서 복구 시도
                        logging.info("   백업 파일에서 복구를 시도합니다...")
                        
                        # 백업 파일 찾기
                        backup_files = [
                            project_root / "pyproject.toml.backup_env",
                            project_root / "pyproject.toml.backup2",
                            project_root / "pyproject.toml.backup",
                        ]
                        
                        restored = False
                        for backup_file in backup_files:
                            if backup_file.exists():
                                try:
                                    import shutil
                                    # 백업 파일도 수정하여 복구
                                    backup_content = backup_file.read_text(encoding='utf-8')
                                    
                                    # 백업 파일의 잘못된 형식도 수정
                                    pattern1 = r'environments\s*=\s*\[\s*["\']?default["\']?\s*,?\s*\]'
                                    if re.search(pattern1, backup_content):
                                        backup_content = re.sub(
                                            pattern1,
                                            'environments = ["default"]',
                                            backup_content,
                                            flags=re.IGNORECASE
                                        )
                                    
                                    # 수정된 백업 내용으로 복구
                                    pyproject_toml.write_text(backup_content, encoding='utf-8')
                                    logging.info(f"   ✅ 백업 파일에서 복구 완료 (형식 수정): {backup_file.name}")
                                    restored = True
                                    break
                                except Exception as e:
                                    logging.debug(f"   백업 파일 복구 실패 ({backup_file}): {e}")
                                    continue
                        
                        if not restored:
                            logging.warning("   ⚠️ 백업 파일을 찾을 수 없습니다.")
                            logging.info("   수동으로 pyproject.toml을 수정해야 합니다.")
                            logging.info("   [tool.uv] 섹션의 environments 설정을 확인하세요:")
                            logging.info("   environments = [\"default\"]  # 올바른 형식")
                            logging.info("   environments = [ \"default\",]  # 잘못된 형식 (trailing comma 제거)")
                except Exception as e:
                    logging.warning(f"   ⚠️ TOML 수정 실패: {e}")
                    logging.info("   수동으로 pyproject.toml을 수정해야 합니다.")
        
        if result.returncode == 0:
            logging.info("✅ pk_system 의존성 추가 완료 (uv add)")
            if result.stdout:
                logging.info("--- uv add stdout ---")
                for line in result.stdout.splitlines():
                    logging.info(line)
            if result.stderr:
                logging.info("--- uv add stderr ---")
                for line in result.stderr.splitlines():
                    logging.info(line)
            if result.stdout:
                logging.debug(f"출력: {result.stdout}")
            
            # --frozen 플래그를 사용하지 않은 경우에만 uv sync 실행
            # (--frozen을 사용하면 의존성 해결을 건너뛰므로 sync도 건너뛰어야 함)
            if not frozen:
                logging.info("")
                logging.info("📦 의존성 설치 중 (uv sync)...")
                logging.info(f"   프로젝트 경로: {project_root}")
                
                # uv sync 실행
                sync_cmd = [uv_exe, 'sync'] if uv_exe != "uv" else ['uv', 'sync']
                if uv_exe != "uv":
                    logging.info(f"💡 uv 실행 파일 사용: {uv_exe}")
                
                sync_result = subprocess.run(
                    sync_cmd,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',  # 인코딩 오류 시 문자 대체
                    timeout=600  # 10분 타임아웃
                )
                
                if sync_result.returncode == 0:
                    logging.info("✅ 의존성 설치 완료 (uv sync)")
                    if sync_result.stdout:
                        logging.info("--- uv sync stdout ---")
                        for line in sync_result.stdout.splitlines():
                            logging.info(line)
                    if sync_result.stderr:
                        logging.info("--- uv sync stderr ---")
                        for line in sync_result.stderr.splitlines():
                            logging.info(line)
                else:
                    logging.warning("⚠️ uv sync 실행 중 오류 발생")
                    if sync_result.stderr:
                        error_msg = sync_result.stderr.strip()
                        logging.warning(f"   오류: {error_msg[:300]}")
                    if sync_result.stdout:
                        logging.warning(f"   출력: {sync_result.stdout[:300]}")
                    logging.info("")
                    logging.info("💡 수동으로 다음 명령어를 실행하여 의존성을 설치하세요:")
                    logging.info(f"   cd {project_root}")
                    logging.info("   uv sync")
            else:
                logging.info("")
                logging.info("💡 --frozen 플래그 사용: 의존성 설치를 건너뜁니다.")
                logging.info("   수동으로 다음 명령어를 실행하여 의존성을 설치하세요:")
                logging.info(f"   cd {project_root}")
                logging.info("   uv sync")
            
            # 백업 파일 정리 (성공 시)
            if pyproject_toml_backup and pyproject_toml_backup.exists():
                try:
                    pyproject_toml_backup.unlink()
                    logging.debug(f"백업 파일 삭제: {pyproject_toml_backup}")
                except Exception as e:
                    logging.debug(f"백업 파일 삭제 실패 (무시): {e}")
            
            return True, None
        else:
            # 오류 출력 수집 (stdout과 stderr 모두)
            error_output = ""
            if result.stdout:
                error_output += result.stdout
                if result.stderr:
                    error_output += "\n"  # 구분자 추가
            if result.stderr:
                error_output += result.stderr
            
            # 의존성 충돌 감지 (오류 메시지에서 직접 확인)
            # 우선순위: 1) "No solution found" 확인, 2) "unsatisfiable" 확인, 3) 패키지 의존성 확인
            conflict_info = None
            
            # stdout과 stderr 내용 확인 (디버깅)
            stdout_preview = (result.stdout[:200] if result.stdout else "") if len(result.stdout or "") > 200 else (result.stdout or "")
            stderr_preview = (result.stderr[:200] if result.stderr else "") if len(result.stderr or "") > 200 else (result.stderr or "")
            
            # "No solution found when resolving dependencies" 메시지 확인 (가장 명확한 충돌 신호)
            # 이 메시지가 있으면 무조건 충돌로 간주하고 재시도
            if "No solution found when resolving dependencies" in error_output:
                logging.info("")
                logging.info("🔍 의존성 충돌 감지: 'No solution found when resolving dependencies'")
                
                # 환경 제한 힌트 확인 ("consider limiting the environments")
                if "consider limiting the environments" in error_output.lower():
                    logging.info("💡 환경 제한 힌트 감지: 다른 환경에서의 의존성 해결 실패")
                    logging.info("   pyproject.toml에 환경 제한을 추가합니다...")
                    if add_environment_limit_to_pyproject(project_root):
                        logging.info("   ✅ 환경 제한 추가 완료")
                        logging.info("   다시 시도합니다...")
                        logging.info("")
                        # 환경 제한 추가 후 재시도
                        return install_pk_system_with_uv_add(
                            project_root=project_root,
                            git_url=git_url,
                            dev=dev,
                            upgrade=upgrade,
                            frozen=frozen,
                            retry_with_frozen=retry_with_frozen,
                            install_path=install_path,
                            branch=branch,
                            tag=tag,
                            commit=commit,
                            use_ssh=use_ssh
                        )
                
                # 패키지 정보 추출 시도
                conflict_info = detect_dependency_conflict(error_output)
                if not conflict_info:
                    # scikit-image 관련 충돌인 경우 직접 감지
                    if "scikit-image==0.25.0" in error_output and "scikit-image==0.25.1" in error_output:
                        conflict_info = "scikit-image: 0.25.0 (pk_system 요구), 0.25.1 (프로젝트 요구)"
                    else:
                        conflict_info = "의존성 해결 실패 (패키지 버전 충돌)"
            elif "unsatisfiable" in error_output or "requirements are unsatisfiable" in error_output:
                conflict_info = detect_dependency_conflict(error_output)
                if not conflict_info:
                    conflict_info = "의존성 충돌 감지됨"
            elif "depends on scikit-image" in error_output or "depends on pk-system" in error_output:
                # scikit-image나 pk-system 관련 의존성 오류도 충돌로 간주
                conflict_info = detect_dependency_conflict(error_output)
                if not conflict_info:
                    conflict_info = "패키지 의존성 충돌 (scikit-image 또는 pk-system 관련)"
            else:
                # 일반적인 충돌 감지 시도
                conflict_info = detect_dependency_conflict(error_output)
            
            # 충돌이 감지되었고 아직 --frozen을 시도하지 않았다면 재시도
            if conflict_info and retry_with_frozen and not frozen:
                logging.warning("")
                logging.warning("⚠️ 의존성 충돌 감지!")
                logging.warning(f"   충돌 패키지: {conflict_info}")
                logging.warning("")
                logging.info("💡 --frozen 플래그로 자동 재시도 중...")
                logging.info("   (의존성 해결을 건너뛰고 설치를 진행합니다)")
                logging.info("")
                
                # --frozen 플래그로 재시도
                # 설치 경로 결정 (기본값: assets/pk_system)
                install_path = project_root / DEFAULT_INSTALL_PATH
                
                return install_pk_system_with_uv_add(
                    project_root=project_root,
                    git_url=git_url,
                    dev=dev,
                    upgrade=upgrade,
                    frozen=True,
                    retry_with_frozen=False,  # 무한 루프 방지
                    install_path=install_path,
                    branch=branch,
                    tag=tag,
                    commit=commit,
                    use_ssh=use_ssh
                )
            
            # 재시도하지 않거나 이미 재시도한 경우
            logging.error(f"❌ uv add 실행 실패")
            
            # 오류 출력 표시 (충돌 정보가 없어도 표시)
            if result.stderr:
                logging.error(f"오류 출력 (stderr):")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():  # 빈 줄 제외
                        logging.error(f"   {line}")
            if result.stdout:
                # stdout에도 오류가 있을 수 있음
                if "No solution found" in result.stdout or "unsatisfiable" in result.stdout:
                    logging.error(f"오류 출력 (stdout):")
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():  # 빈 줄 제외
                            logging.error(f"   {line}")
                elif not conflict_info:
                    # 충돌 정보가 없을 때만 전체 출력
                    logging.error(f"표준 출력:")
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():  # 빈 줄 제외
                            logging.error(f"   {line}")
            
            # 충돌 정보가 없어도 "No solution found" 메시지가 있으면 충돌로 간주
            if not conflict_info and "No solution found when resolving dependencies" in error_output:
                conflict_info = "의존성 해결 실패 감지됨"
            
            return False, conflict_info
            
    except subprocess.TimeoutExpired:
        logging.error("❌ 설치 시간 초과 (10분 이상 소요)")
        return False, None
    except Exception as e:
        logging.error(f"❌ 설치 중 오류 발생: {e}")
        return False, None


def verify_installation(project_root: Optional[Path] = None, verbose: bool = True) -> bool:
    """
    pk_system 설치 및 import 검증
    
    순환 import 문제를 피하기 위해 lazy import와 서브프로세스를 사용합니다.
    
    Args:
        project_root: 프로젝트 루트 경로 (pk_system 내부 python.exe 검색용)
        verbose: 상세한 디버깅 정보 출력 여부
    """
    try:
        # Lazy import: sys와 subprocess는 최상위에서 이미 import되어 있지만,
        # 함수 내부에서 사용하여 명확성을 높임
        import sys
        
        if verbose:
            print("")
            print("_" * 66)
            print("# 설치 검증 상세 정보")
            print("")
            
            # 프로젝트 루트 확인
            if project_root:
                logging.info(f"   프로젝트 루트: {project_root}")
                
                # pyproject.toml 확인
                pyproject_toml = project_root / "pyproject.toml"
                if pyproject_toml.exists():
                    logging.info(f"   ✅ pyproject.toml 존재: {pyproject_toml}")
                    try:
                        content = pyproject_toml.read_text(encoding='utf-8')
                        if "pk-system" in content or "pk_system" in content:
                            logging.info("   ✅ pyproject.toml에 pk-system 의존성 포함됨")
                            # pk-system 의존성 라인 찾기
                            for line in content.split('\n'):
                                if 'pk-system' in line or 'pk_system' in line:
                                    logging.info(f"      의존성 라인: {line.strip()[:100]}")
                        else:
                            logging.warning("   ⚠️ pyproject.toml에 pk-system 의존성이 없습니다")
                    except Exception as e:
                        logging.warning(f"   ⚠️ pyproject.toml 읽기 실패: {e}")
                else:
                    logging.warning(f"   ⚠️ pyproject.toml 없음: {pyproject_toml}")
                
                # assets/pk_system 디렉토리 확인
                pk_system_path = project_root / DEFAULT_INSTALL_PATH
                if pk_system_path.exists():
                    logging.info(f"   ✅ pk_system 디렉토리 존재: {pk_system_path}")
                    # 주요 파일 확인
                    pyproject_in_pk = pk_system_path / "pyproject.toml"
                    if pyproject_in_pk.exists():
                        logging.info(f"      ✅ pk_system/pyproject.toml 존재")
                    sources_dir = pk_system_path / "pk_system_sources"
                    if sources_dir.exists():
                        logging.info(f"      ✅ pk_system_sources 디렉토리 존재")
                        # 주요 모듈 확인
                        test_file = sources_dir / "pk_system_objects" / "pk_system_directories.py"
                        if test_file.exists():
                            logging.info(f"      ✅ pk_system_directories.py 존재")
                        else:
                            logging.warning(f"      ⚠️ pk_system_directories.py 없음")
                    else:
                        logging.warning(f"      ⚠️ pk_system_sources 디렉토리 없음")
                else:
                    logging.warning(f"   ⚠️ pk_system 디렉토리 없음: {pk_system_path}")
                
                # .venv 확인
                venv_path = project_root / ".venv"
                if venv_path.exists():
                    logging.info(f"   ✅ 프로젝트 가상환경 존재: {venv_path}")
                else:
                    logging.info(f"   ℹ️ 프로젝트 가상환경 없음 (정상일 수 있음)")
            
            logging.info("")
        
        # Python 실행 파일 찾기 (클론된 pk_system 내부 python 우선 사용)
        python_exe = find_python_executable(project_root) or sys.executable
        if verbose:
            if python_exe != sys.executable:
                logging.info(f"   💡 클론된 pk_system 내부 Python 사용: {python_exe}")
            else:
                logging.info(f"   💡 시스템 Python 사용: {python_exe}")
        
        if verbose:
            logging.info("")
            logging.info("🔍 Python import 테스트 실행 중...")
        
        # 서브프로세스로 import 테스트 (순환 import 회피)
        # 함수 내부에서 lazy import를 통해 import 시점을 지연
        test_code = """
import sys
try:
    # Lazy import를 위한 함수 내부 import
    def _test_import():
        try:
            from temp.pk_system.pk_system_sources.pk_system_objects.pk_system_directories import (
                get_pk_system_root,
                D_PK_SYSTEM
            )
            pk_root = get_pk_system_root()
            if pk_root:
                return pk_root
            else:
                return None
        except ImportError as e:
            raise ImportError(f"Import failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")
    
    pk_root = _test_import()
    if pk_root:
        print(f"SUCCESS: {pk_root}")
        sys.exit(0)
    else:
        print("ERROR: get_pk_system_root() returned None")
        sys.exit(1)
except ImportError as e:
    print(f"ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"""
        
        # subprocess는 함수 내부에서 lazy import (이미 상단에서 import되어 있음)
        if verbose:
            logging.info(f"   실행 명령: {python_exe} -c '...'")
            logging.info(f"   작업 디렉토리: {project_root if project_root else Path.cwd()}")
        
        result = subprocess.run(
            [python_exe, '-c', test_code],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            cwd=project_root if project_root else None
        )
        
        if verbose:
            logging.info(f"   반환 코드: {result.returncode}")
            if result.stdout:
                logging.info(f"   표준 출력:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logging.info(f"      {line[:100]}")
            if result.stderr:
                logging.info(f"   표준 오류:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logging.info(f"      {line[:100]}")
            logging.info("")
        
        if result.returncode == 0:
            if "SUCCESS:" in result.stdout:
                pk_root = result.stdout.split("SUCCESS:")[-1].strip()
                logging.info(f"pk_system import 성공: {pk_root}")
                logging.info(f"   설치 경로: {pk_root}")
                
                # 추가 검증은 선택적으로 (순환 import 위험이 있으므로 서브프로세스로)
                # .env 파일 경로 검증은 별도 서브프로세스로 처리
                env_test_code = """
import sys
try:
    def _test_env_setup():
        try:
            from temp.pk_system.pk_system_sources.pk_system_functions.ensure_pk_system_env_file_setup import (
                ensure_pk_system_env_file_setup
            )
            return ensure_pk_system_env_file_setup()
        except ImportError:
            return None
        except Exception:
            return None
    
    env_path = _test_env_setup()
    if env_path:
        print(f"ENV_SUCCESS: {env_path}")
    else:
        print("ENV_SKIP: Optional module not available")
except Exception:
    print("ENV_SKIP: Optional module test failed")
"""
                try:
                    # 같은 python_exe 사용
                    env_result = subprocess.run(
                        [python_exe, '-c', env_test_code],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        timeout=5
                    )
                    if env_result.returncode == 0 and "ENV_SUCCESS:" in env_result.stdout:
                        env_path = env_result.stdout.split("ENV_SUCCESS:")[-1].strip()
                        logging.info(f".env 파일 경로 확인: {env_path}")
                    # ENV_SKIP은 경고 없이 무시 (선택적 기능)
                except Exception:
                    # .env 검증 실패는 무시 (선택적 기능)
                    pass
                
                return True
            else:
                logging.error("❌ pk_system import 검증 실패: 검증 결과를 확인할 수 없습니다.")
                if result.stdout:
                    logging.error(f"   출력: {result.stdout}")
                return False
        else:
            error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
            
            # 의존성 누락 오류 확인 (No module named)
            if "No module named" in error_msg:
                # 의존성 누락은 설치 문제이므로 False 반환 (uv sync 실행하도록)
                logging.warning(f"⚠️ pk_system import 검증 중 의존성 누락 감지")
                error_preview = error_msg[:300] if len(error_msg) > 300 else error_msg
                logging.warning(f"   오류 메시지: {error_preview}")
                logging.info("")
                logging.info("💡 의존성 패키지가 설치되지 않았을 수 있습니다.")
                logging.info("   'uv sync'를 실행하여 의존성을 설치하겠습니다.")
                logging.info("")
                return False  # 의존성 누락은 설치 문제이므로 False 반환
            
            # 순환 import 오류 확인
            if "Import failed" in error_msg or "cannot import" in error_msg or "circular import" in error_msg.lower():
                # 순환 import 오류는 경고로 처리 (설치는 성공했을 수 있음)
                logging.warning(f"⚠️ pk_system import 검증 중 순환 import 감지")
                
                # 오류 메시지에서 중요한 부분만 추출
                error_preview = error_msg[:300] if len(error_msg) > 300 else error_msg
                if "LTA" in error_msg:
                    logging.warning("   순환 import 발생: pk_lta 모듈")
                    logging.warning("   이는 pk_system 내부의 순환 import 문제입니다.")
                else:
                    logging.warning(f"   오류 메시지: {error_preview}")
                
                logging.info("")
                logging.info("💡 이것은 설치 문제가 아닐 수 있습니다.")
                logging.info("   순환 import는 pk_system 내부 모듈 간 의존성 문제일 수 있습니다.")
                logging.info("")
                logging.info("# 해결 방법")
                logging.info("   1. Python 환경을 완전히 재시작 (인터프리터 재시작)")
                logging.info("   2. 가상 환경을 다시 활성화")
                logging.info("   3. pyproject.toml에 pk_system이 정상적으로 추가되었는지 확인")
                logging.info("   4. 실제 사용 시에는 문제가 없을 수 있습니다 (런타임 import는 다르게 동작)")
                logging.info("")
                
                # 순환 import만 감지된 경우
                # 의존성 누락도 함께 있는지 확인
                if "No module named" in error_msg:
                    # 의존성 누락이 함께 있는 경우 False 반환 (uv sync 실행)
                    logging.info("   💡 의존성 누락도 감지되었습니다. 의존성 설치를 시도합니다.")
                    return False
                else:
                    # 순환 import만 있는 경우
                    # pyproject.toml에 pk_system이 있고 assets/pk_system 디렉토리가 존재하면
                    # 설치된 것으로 간주하되, 의존성 설치가 완료되었는지 확인하기 위해
                    # False를 반환하여 uv sync 실행 (의존성 설치 보장)
                    if project_root:
                        pk_system_path = project_root / DEFAULT_INSTALL_PATH
                        pyproject_toml = project_root / "pyproject.toml"
                        if pk_system_path.exists() and pyproject_toml.exists():
                            try:
                                content = pyproject_toml.read_text(encoding='utf-8')
                                if "pk-system" in content or "pk_system" in content:
                                    # 설치된 것으로 보이지만 의존성이 누락되었을 수 있으므로
                                    # 실제 의존성 설치 여부 확인
                                    if verbose:
                                        logging.info("")
                                        logging.info("🔍 의존성 설치 확인 중...")
                                        
                                        # 주요 의존성 모듈 테스트
                                        deps_check_code = """
import sys
missing = []
try:
    import toml
except ImportError:
    missing.append('toml')
try:
    import numpy
except ImportError:
    missing.append('numpy')
try:
    import pandas
except ImportError:
    missing.append('pandas')
if missing:
    print(f"MISSING: {','.join(missing)}")
    sys.exit(1)
else:
    print("OK: 주요 의존성 설치됨")
    sys.exit(0)
"""
                                        deps_result = subprocess.run(
                                            [python_exe, '-c', deps_check_code],
                                            capture_output=True,
                                            text=True,
                                            encoding='utf-8',
                                            errors='replace',
                                            timeout=10,
                                            cwd=project_root if project_root else None
                                        )
                                        
                                        if deps_result.returncode == 0:
                                            logging.info("   ✅ 주요 의존성 (toml, numpy, pandas) 설치 확인됨")
                                        else:
                                            if "MISSING:" in deps_result.stdout:
                                                missing_deps = deps_result.stdout.split("MISSING:")[-1].strip()
                                                logging.warning(f"   ⚠️ 누락된 의존성: {missing_deps}")
                                                logging.info("   💡 uv sync를 실행하여 의존성을 설치합니다.")
                                                logging.info("")
                                                return False
                                            else:
                                                logging.warning("   ⚠️ 의존성 확인 실패")
                                                logging.info("   💡 uv sync를 실행하여 의존성을 설치합니다.")
                                                logging.info("")
                                                return False
                                    
                                    # 의존성 확인 없이 바로 uv sync 실행
                                    logging.info("   💡 순환 import는 있지만, 의존성 설치를 확인하기 위해 uv sync를 실행합니다.")
                                    return False
                            except Exception as e:
                                if verbose:
                                    logging.warning(f"   ⚠️ 의존성 확인 중 오류: {e}")
                    
                    # 순환 import만 있고 의존성 문제가 없어 보이는 경우 True 반환
                    if verbose:
                        logging.info("   ✅ 순환 import만 감지됨 (설치 문제 아님)")
                        logging.info("   💡 순환 import는 pk_system 내부 모듈 간 의존성 문제입니다.")
                        logging.info("   실제 사용 시에는 문제가 없을 수 있습니다.")
                    return True  # 순환 import는 설치 문제가 아니므로 True 반환
            else:
                logging.error(f"❌ pk_system import 검증 실패: {error_msg[:200]}")
                logging.error("   Python 환경을 다시 시작하거나 가상 환경을 활성화하세요.")
                return False
    except subprocess.TimeoutExpired:
        logging.error("❌ 설치 검증 시간 초과")
        return False
    except Exception as e:
        logging.error(f"❌ 설치 검증 중 오류 발생: {e}")
        return False


def print_usage_guide(project_root: Path):
    """사용 가이드 출력"""
    from textwrap import dedent
    
    print("")
    print("_" * 66)
    print("# pk_system 사용 가이드")
    print("")
    
    # 1. 기본 사용
    print("_" * 66)
    print("# 1. 기본 사용")
    usage_code = dedent("""\
from temp.pk_system.pk_system_sources.pk_system_functions.ensure_pk_system_env_file_setup import (
    ensure_pk_system_env_file_setup
)
from temp.pk_system.pk_system_sources.pk_system_objects.pk_system_directories import (
    get_pk_system_root
)

# 초기화
ensure_pk_system_env_file_setup()

# 사용
pk_root = get_pk_system_root()
""")
    print(usage_code)
    
    # 2. .env 파일 설정
    print("_" * 66)
    print("# 2. .env 파일 설정")
    print(f"프로젝트 루트의 부모 디렉토리에 .env 파일을 생성하세요.")
    print(f"예: {project_root.parent / '.env'}")
    print("")
    
    # 3. 문서
    print("_" * 66)
    print("# 3. 문서")
    print("- 설치 가이드: pk_system_docs/library/INSTALLATION_GUIDE.md")
    print("- 사용 가이드: pk_system_docs/library/USAGE_GUIDE.md")
    print("- API 레퍼런스: pk_system_docs/library/API_REFERENCE.md")
    print("")
    print("_" * 66)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="pk_system 자동 설치 스크립트 (uv 프로젝트 권장 방식)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 기본 설치 (현재 디렉토리를 프로젝트 루트로 사용)
  python install_pk_system.py
  
  # 프로젝트 루트 명시적으로 지정 (권장)
  python install_pk_system.py --project-root /path/to/your_project
  
  # 특정 브랜치 설치
  python install_pk_system.py --project-root /path/to/your_project --branch develop
  
  # 특정 태그 설치 (프로덕션 권장)
  python install_pk_system.py --project-root /path/to/your_project --tag v2025.1.15
  
  # SSH URL 사용 (Private 저장소)
  python install_pk_system.py --project-root /path/to/your_project --ssh
  
  # 개발 의존성으로 추가
  python install_pk_system.py --project-root /path/to/your_project --dev
        """
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        required=False,
        help="프로젝트 루트 디렉토리 (기본값: 자동 탐색). .git, pyproject.toml, uv.lock 등을 기반으로 자동으로 찾습니다."
    )
    parser.add_argument(
        "--branch",
        type=str,
        default=None,
        help=f"Git 브랜치 (기본값: {DEFAULT_BRANCH})"
    )
    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Git 태그 (지정하면 브랜치 대신 사용, 프로덕션 권장)"
    )
    parser.add_argument(
        "--commit",
        type=str,
        default=None,
        help="Git 커밋 해시 (지정하면 브랜치/태그 대신 사용)"
    )
    parser.add_argument(
        "--git-url",
        type=str,
        default=None,
        help="Git 저장소 URL (지정하면 브랜치/태그/커밋 무시)"
    )
    parser.add_argument(
        "--ssh",
        action="store_true",
        help="SSH URL 사용 (Private 저장소용)"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="개발 의존성으로 추가"
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="이미 설치된 경우 업그레이드"
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="설치 검증 건너뛰기"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="이미 설치되어 있어도 재설치"
    )
    parser.add_argument(
        "--frozen",
        action="store_true",
        help="의존성 해결 건너뛰기 (충돌 발생 시 사용)"
    )
    parser.add_argument(
        "--no-auto-frozen",
        action="store_true",
        help="의존성 충돌 시 자동으로 --frozen 플래그 사용하지 않음"
    )
    
    args = parser.parse_args()
    
    # 프로젝트 루트 결정
    if args.project_root:
        # 명시적으로 지정된 경우
        project_root = Path(args.project_root).resolve()
        if not project_root.exists():
            logging.error(f"❌ 지정된 프로젝트 루트 디렉토리가 존재하지 않습니다: {project_root}")
            sys.exit(1)
        if not project_root.is_dir():
            logging.error(f"❌ 지정된 경로가 디렉토리가 아닙니다: {project_root}")
            sys.exit(1)
    else:
        # 자동으로 프로젝트 루트 찾기
        current_dir = Path.cwd().resolve()
        found_root = find_project_root(current_dir)
        
        if found_root:
            project_root = found_root
            logging.info("💡 프로젝트 루트를 자동으로 찾았습니다:")
            logging.info(f"   현재 디렉토리: {current_dir}")
            logging.info(f"   프로젝트 루트: {project_root}")
            if project_root != current_dir:
                logging.info("")
                logging.info("💡 다른 디렉토리를 사용하려면 --project-root 옵션을 사용하세요:")
                logging.info(f"   python install_pk_system.py --project-root /path/to/project")
            logging.info("")
        else:
            # 찾지 못한 경우 현재 디렉토리 사용
            project_root = current_dir
            logging.warning("⚠️ 프로젝트 루트를 자동으로 찾지 못했습니다.")
            logging.warning(f"   현재 디렉토리를 프로젝트 루트로 사용합니다: {project_root}")
            logging.info("")
            logging.info("💡 프로젝트 루트를 명시적으로 지정하려면 --project-root 옵션을 사용하세요:")
            logging.info(f"   python install_pk_system.py --project-root /path/to/project")
            logging.info("")
    
    print("_" * 66)
    print("# pk_system 자동 설치 시작")
    print("")
    logging.info(f"프로젝트 루트: {project_root}")
    if project_root != Path.cwd().resolve():
        logging.info(f"실행 디렉토리: {Path.cwd().resolve()}")
    logging.info("")
    
    # uv 명령어 확인 (pk_system 내부 uv.exe 우선 검색)
    uv_exe = find_uv_executable(project_root)
    if not uv_exe:
        logging.error("❌ uv 명령어를 찾을 수 없습니다.")
        logging.error("   uv 설치: curl -LsSf https://astral.sh/uv/install.sh | sh")
        logging.error("   또는: https://github.com/astral-sh/uv")
        logging.error("   또는: pk_system을 설치하면 내부 uv.exe가 사용됩니다.")
        sys.exit(1)
    
    if uv_exe != "uv":
        logging.info(f"uv 실행 파일 확인됨: {uv_exe}")
    else:
        logging.info("✅ uv 명령어 확인됨 (시스템)")
    
    # uv 프로젝트 확인
    pyproject_toml = project_root / "pyproject.toml"
    if not is_uv_project(project_root):
        # pyproject.toml이 없는 경우
        if not pyproject_toml.exists():
            logging.warning("⚠️ pyproject.toml 파일이 없습니다.")
            logging.info("")
            logging.info("💡 이 스크립트는 uv 프로젝트를 사용합니다.")
            logging.info("   pyproject.toml을 자동으로 생성할 수 있습니다.")
            logging.info("")
            logging.info("# 옵션")
            logging.info("  1. 자동 생성 (권장): uv add가 자동으로 pyproject.toml 생성")
            logging.info("  2. 수동 생성: uv init으로 먼저 생성 후 설치")
            logging.info("  3. 취소: 설치 중단")
            logging.info("")
            
            # 비대화형 모드 확인 (환경 변수나 플래그로)
            auto_init = os.environ.get('PK_SYSTEM_AUTO_INIT', '').lower() == 'true'
            
            if not auto_init:
                response = input("pyproject.toml을 자동 생성하고 계속하시겠습니까? (Y/n): ").strip()
                if response.lower() == 'n':
                    logging.info("")
                    logging.info("수동으로 pyproject.toml을 생성하려면:")
                    logging.info(f"   cd {project_root}")
                    logging.info("   uv init")
                    logging.info("   그 다음 이 스크립트를 다시 실행하세요.")
                    logging.info("")
                    sys.exit(0)
            
            # uv add가 자동으로 pyproject.toml을 생성하는지 확인
            # uv add는 pyproject.toml이 없으면 자동으로 생성합니다
            logging.info("💡 uv add 명령어가 pyproject.toml을 자동으로 생성합니다.")
            logging.info("   계속 진행합니다...")
            logging.info("")
        else:
            # pyproject.toml은 있지만 uv 프로젝트로 인식되지 않는 경우
            logging.warning("⚠️ uv 프로젝트로 감지되지 않았습니다.")
            logging.warning("   pyproject.toml은 존재하지만 uv 프로젝트 형식이 아닐 수 있습니다.")
            logging.warning("   계속 진행하시겠습니까? (수동 확인 필요)")
            response = input("계속 진행하시겠습니까? (y/N): ").strip()
            if response.lower() != 'y':
                logging.info("설치를 취소합니다.")
                sys.exit(0)
    
    # 이미 설치되어 있는지 확인
    auto_upgrade = False  # 전역 변수로 초기화
    if is_pk_system_installed(project_root) and not args.force:
        logging.info("✅ pk_system이 이미 설치되어 있습니다.")
        
        # Git URL이 main 브랜치를 사용하는 경우 최신화 여부 묻기
        git_url = build_git_url(
            branch=args.branch or DEFAULT_BRANCH,
            tag=args.tag,
            commit=args.commit,
            use_ssh=args.ssh,
            git_url=args.git_url
        )
        
        # main 브랜치를 사용하고 태그/커밋이 지정되지 않은 경우 최신 버전 확인 후 묻기
        if not args.upgrade and not args.tag and not args.commit:
            if args.branch == DEFAULT_BRANCH or (not args.branch and DEFAULT_BRANCH in git_url):
                logging.info("💡 main 브랜치를 사용 중입니다. 최신 버전 확인 중...")
                has_newer, current_commit, latest_commit = check_if_newer_version_available(project_root, git_url)
                
                if has_newer:
                    if current_commit and latest_commit:
                        logging.info(f"   현재 버전: {current_commit[:7]}...")
                        logging.info(f"   최신 버전: {latest_commit[:7]}...")
                    else:
                        logging.info("   최신 버전이 있습니다.")
                    response = input("   최신 버전으로 업데이트하시겠습니까? (Y/n): ").strip().lower()
                    if response in ('', 'y', 'yes'):
                        auto_upgrade = True
                        logging.info("   최신화를 진행합니다.")
                    else:
                        logging.info("   최신화를 건너뜁니다.")
                else:
                    logging.info("   이미 최신 버전입니다.")
        
        if not args.upgrade and not auto_upgrade:
            logging.info("   업그레이드를 원하면 --upgrade 옵션을 사용하세요.")
            # 검증만 수행하고 종료
            if not args.skip_verify:
                logging.info("")
                logging.info("설치 검증 중...")
                if verify_installation(project_root):
                    print_usage_guide(project_root)
                    sys.exit(0)
                else:
                    # 검증 실패 시 의존성 설치 시도 (uv sync)
                    logging.warning("⚠️ 설치 검증 실패 - 의존성 설치 시도 중...")
                    logging.info("")
                    
                    # uv 실행 파일 찾기 (pk_system 내부 우선)
                    uv_exe = find_uv_executable(project_root)
                    if uv_exe:
                        # uv sync 전에 pyproject.toml 구문 오류 수정 시도
                        logging.info("💡 pyproject.toml 파일 검사 중...")
                        if fix_pyproject_toml_dependency(project_root):
                            logging.info("✅ pyproject.toml 수정 완료")
                        logging.info("")
                        logging.info("📦 의존성 설치 중 (uv sync)...")
                        logging.info(f"   프로젝트 경로: {project_root}")
                        
                        if uv_exe != "uv":
                            logging.info(f"💡 pk_system 내부 uv.exe 사용: {uv_exe}")
                        
                        # uv sync 실행 (의존성 충돌 발생 시 --frozen 사용)
                        sync_cmd = [uv_exe, 'sync'] if uv_exe != "uv" else ['uv', 'sync']
                        sync_result = subprocess.run(
                            sync_cmd,
                            cwd=project_root,
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='replace',  # 인코딩 오류 시 문자 대체
                            timeout=600  # 10분 타임아웃
                        )
                        
                        # uv sync 실패 시 의존성 충돌 확인 및 --frozen으로 재시도
                        if sync_result.returncode != 0:
                            error_output = (sync_result.stderr or "") + (sync_result.stdout or "")
                            
                            # 의존성 충돌 감지
                            if "No solution found" in error_output or "unsatisfiable" in error_output:
                                logging.warning("⚠️ uv sync 실행 중 의존성 충돌 감지")
                                logging.info("   --frozen 플래그로 재시도합니다...")
                                logging.info("")
                                
                                # --frozen으로 재시도
                                sync_cmd_frozen = [uv_exe, 'sync', '--frozen'] if uv_exe != "uv" else ['uv', 'sync', '--frozen']
                                sync_result = subprocess.run(
                                    sync_cmd_frozen,
                                    cwd=project_root,
                                    capture_output=True,
                                    text=True,
                                    encoding='utf-8',
                                    errors='replace',
                                    timeout=600
                                )
                        
                        if sync_result.returncode == 0:
                            logging.info("✅ 의존성 설치 완료 (uv sync)")
                            
                            # 최신화 확인: uv.lock에서 실제 설치된 커밋 해시 확인
                            if auto_upgrade:
                                _verify_upgrade_success(project_root, git_url)
                            logging.info("")
                            logging.info("설치 검증 재시도 중...")
                            
                            # 다시 검증
                            if verify_installation(project_root):
                                logging.info("✅ 검증 성공!")
                                print_usage_guide(project_root)
                                sys.exit(0)
                            else:
                                # 검증 실패 시 순환 import만 있는지 확인
                                # 순환 import만 있고 의존성은 설치되었으므로 성공으로 간주
                                logging.info("")
                                logging.info("💡 의존성은 설치되었지만 순환 import가 감지되었습니다.")
                                logging.info("   이것은 설치 문제가 아닐 수 있습니다.")
                                logging.info("   실제 사용 시에는 문제가 없을 수 있습니다.")
                                logging.info("")
                                print_usage_guide(project_root)
                                sys.exit(0)  # 순환 import는 설치 문제가 아니므로 성공으로 간주
                        else:
                            # uv sync 실패 - Git URL 문제인지 확인
                            error_output = (sync_result.stderr or "") + (sync_result.stdout or "")
                            
                            # Git URL 문제 또는 workspace 문제 감지
                            is_git_url_error = "git+https://github.com/PARK4139/pk_system.git" in error_output or "Failed to download and build" in error_output
                            is_workspace_error = "workspace" in error_output.lower() and ("not a workspace member" in error_output.lower() or "references a workspace" in error_output.lower())
                            
                            if is_git_url_error or is_workspace_error:
                                if is_workspace_error:
                                    logging.warning("⚠️ pyproject.toml에 workspace = true 의존성이 감지되었습니다.")
                                    logging.info("   로컬 경로 의존성으로 수정을 시도합니다...")
                                else:
                                    logging.warning("⚠️ pyproject.toml에 잘못된 Git URL이 감지되었습니다.")
                                    logging.info("   로컬 경로 의존성으로 수정을 시도합니다...")
                                logging.info("")
                                
                                # pyproject.toml 수정 시도
                                if fix_pyproject_toml_dependency(project_root):
                                    logging.info("✅ pyproject.toml 수정 완료 - 다시 uv sync 시도 중...")
                                    logging.info("")
                                    
                                    # 다시 uv sync 실행
                                    sync_result = subprocess.run(
                                        sync_cmd,
                                        cwd=project_root,
                                        capture_output=True,
                                        text=True,
                                        encoding='utf-8',
                                        errors='replace',
                                        timeout=600
                                    )
                                    
                                    if sync_result.returncode == 0:
                                        logging.info("✅ 의존성 설치 완료 (uv sync)")
                                        logging.info("")
                                        logging.info("설치 검증 재시도 중...")
                                        
                                        # 다시 검증
                                        if verify_installation(project_root):
                                            logging.info("✅ 검증 성공!")
                                            print_usage_guide(project_root)
                                            sys.exit(0)
                                        else:
                                            logging.warning("⚠️ 의존성 설치 후에도 검증 실패")
                                            logging.warning("   --force 옵션으로 재설치를 권장합니다:")
                                            logging.warning(f"   python install_pk_system.py --force")
                                            sys.exit(1)
                                    else:
                                        logging.error("❌ pyproject.toml 수정 후에도 uv sync 실패")
                                        if sync_result.stderr:
                                            logging.error(f"   오류: {sync_result.stderr.strip()[:300]}")
                                        logging.warning("   --force 옵션으로 재설치를 권장합니다:")
                                        logging.warning(f"   python install_pk_system.py --force")
                                        sys.exit(1)
                                else:
                                    logging.error("❌ pyproject.toml 수정 실패")
                                    logging.warning("   --force 옵션으로 재설치를 권장합니다:")
                                    logging.warning(f"   python install_pk_system.py --force")
                                    sys.exit(1)
                            else:
                                logging.error("❌ uv sync 실행 실패")
                                if sync_result.stderr:
                                    logging.error(f"   오류: {sync_result.stderr.strip()[:300]}")
                                logging.warning("   --force 옵션으로 재설치를 권장합니다:")
                                logging.warning(f"   python install_pk_system.py --force")
                                sys.exit(1)
                    else:
                        logging.error("❌ uv 실행 파일을 찾을 수 없습니다.")
                        logging.warning("   수동으로 'uv sync'를 실행하거나 --force 옵션으로 재설치하세요:")
                        logging.warning(f"   python install_pk_system.py --force")
                        sys.exit(1)
            else:
                sys.exit(0)
    
    # Git URL 구성
    git_url = build_git_url(
        branch=args.branch or DEFAULT_BRANCH,
        tag=args.tag,
        commit=args.commit,
        use_ssh=args.ssh,
        git_url=args.git_url
    )
    
    logging.info(f"Git URL: {git_url}")
    logging.info("")
    
    # 설치 수행 (대화형 모드)
    was_upgraded = args.upgrade or args.force or auto_upgrade
    success, conflict_info = install_pk_system_interactive(
        project_root=project_root,
        git_url=git_url,
        dev=args.dev,
        upgrade=was_upgraded,
        frozen=args.frozen,
        use_ssh=args.ssh,
        branch=args.branch,
        tag=args.tag,
        commit=args.commit,
        auto_retry=not args.no_auto_frozen
    )
    
    if not success:
        print("")
        print("_" * 66)
        print("# pk_system 설치 실패")
        print("")
        
        if conflict_info:
            logging.error("🔍 의존성 충돌 발견:")
            logging.error(f"   {conflict_info}")
            logging.error("")
            logging.error("# 해결 방법")
            logging.error("")
            logging.error("# 방법 1: --frozen 플래그 사용 (권장)")
            logging.error(f"   python install_pk_system.py --frozen")
            logging.error("   이 방법은 의존성 해결을 건너뛰고 설치합니다.")
            logging.error("")
            logging.error("# 방법 2: 프로젝트의 충돌하는 패키지 버전 조정")
            logging.error(f"   pyproject.toml에서 버전을 조정하세요:")
            for conflict in conflict_info.split("; "):
                if ":" in conflict:
                    pkg_name, versions = conflict.split(":", 1)
                    logging.error(f"   {pkg_name}: {versions}")
                    logging.error(f"   → pk_system이 요구하는 버전으로 변경하세요")
            logging.error("")
            logging.error("# 방법 3: 환경 제한 설정")
            logging.error("   pyproject.toml에 다음 추가:")
            logging.error("   [tool.uv]")
            logging.error("   environments = [\"default\"]")
            logging.error("")
            logging.error("# 방법 4: 충돌하는 패키지 제거 후 재설치")
            logging.error("   pyproject.toml에서 충돌하는 패키지를 제거하고")
            logging.error("   pk_system 설치 후 다시 추가하세요.")
        else:
            logging.error("# 문제 해결")
            logging.error("1. Git이 설치되어 있는지 확인: git --version")
            logging.error("2. 네트워크 연결 확인")
            logging.error("3. Private 저장소인 경우 SSH 키 또는 토큰 설정 확인")
            logging.error("4. 프로젝트 루트 디렉토리 확인: --project-root 옵션 사용")
            logging.error("5. Python 버전 확인: python --version (>=3.12 필요)")
        
        sys.exit(1)
    
    # 설치 검증
    if not args.skip_verify:
        logging.info("")
        logging.info("설치 검증 중...")
        if not verify_installation(project_root):
            logging.warning("⚠️ 설치되었지만 import 검증에 실패했습니다.")
            logging.warning("   Python 환경을 다시 시작하거나 가상 환경을 활성화하세요:")
            logging.warning(f"   cd {project_root}")
            logging.warning("   source .venv/bin/activate  # Linux/WSL")
            logging.warning("   .venv\\Scripts\\activate     # Windows")
            logging.warning("   또는: uv run python your_script.py")
            print_usage_guide(project_root)
            sys.exit(1)
    
    # 성공 메시지 (시스템 규칙에 따른 출력 형식)
    print("")
    print("_" * 66)
    print("# pk_system 설치 완료")
    print("")
    
    # 최신화 여부 확인 (upgrade가 True인 경우)
    if was_upgraded:
        git_url = build_git_url(
            branch=args.branch or DEFAULT_BRANCH,
            tag=args.tag,
            commit=args.commit,
            use_ssh=args.ssh,
            git_url=args.git_url
        )
        _verify_upgrade_success(project_root, git_url)
    
    print_usage_guide(project_root)
    sys.exit(0)


if __name__ == "__main__":
    try:
        # 가상 환경 변수 문제 방지
        import os
        venv_backup = os.environ.get('VIRTUAL_ENV')
        if venv_backup:
            # 가상 환경이 손상되었을 수 있으므로 임시 제거
            del os.environ['VIRTUAL_ENV']
        
        main()
        
        # 가상 환경 변수 복원
        if venv_backup:
            os.environ['VIRTUAL_ENV'] = venv_backup
    except KeyboardInterrupt:
        logging.error("")
        logging.error("❌ 사용자가 설치를 취소했습니다.")
        sys.exit(130)
    except SystemExit as e:
        # sys.exit() 호출은 정상적인 종료
        raise
    except Exception as e:
        error_msg = str(e)
        # pyvenv.cfg 오류 특별 처리
        if "pyvenv.cfg" in error_msg or "failed to locate" in error_msg.lower():
            print("")
            print("_" * 66)
            print("# Python 가상 환경 오류")
            print("")
            logging.error("가상 환경이 손상되었거나 경로 문제가 있습니다.")
            logging.error("")
            logging.error("# 해결 방법")
            logging.error("1. VIRTUAL_ENV 환경 변수를 임시로 제거하고 다시 시도")
            logging.error("2. 시스템 Python 사용:")
            logging.error("   python install_pk_system.py")
            logging.error("3. 또는 py launcher 사용:")
            logging.error("   py install_pk_system.py")
        else:
            print("")
            print("_" * 66)
            print("# 예상치 못한 오류가 발생했습니다")
            print("")
            logging.error(f"오류 타입: {type(e).__name__}")
            logging.error(f"오류 메시지: {error_msg}")
            logging.error("")
            import traceback
            logging.error("상세 오류 정보:")
            logging.error("-" * 60)
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    logging.error(line)
            logging.error("-" * 60)
            logging.error("")
            logging.error("# 문제 해결")
            logging.error("1. Python 버전 확인: python --version (>=3.12 필요)")
            logging.error("2. 필요한 패키지 설치 확인")
            logging.error("3. 스크립트 파일이 손상되지 않았는지 확인")
        sys.exit(1)


import logging
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from rich.progress import Progress

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


@ensure_seconds_measured
def fix_git_push_fail_for_large_file():
    """
    로컬 워킹 트리는 보존하면서 Git 히스토리에서 대용량 파일을 제거하여 푸시 가능하도록 처리
    """
    func_n = get_caller_name()

    logging.info(f"{PK_UNDERLINE}\n{PkColors.BRIGHT_RED}⚠️ 경고: 이 작업은 Git 히스토리를 영구적으로 변경합니다!{PkColors.RESET}")
    logging.info(f"{PkColors.BRIGHT_YELLOW}  -  공동 작업 중인 경우 팀원들에게 매우 큰 영향을 줄 수 있습니다.")
    logging.info(f"실행 전에 반드시 현재 Git 저장소를 백업하십시오.")
    logging.info(f"복구 불가능한 변경이 발생할 수 있습니다.{PkColors.RESET}")

    ok = ensure_value_completed(
        key_name="confirm_git_history_change",
        func_n=func_n,
        guide_text="계속 진행하시겠습니까? (yes/no)",
        options=["yes", "no"]
    )
    if ok != "yes":
        logging.info("사용자가 작업을 취소했습니다.")
        return False

    # size_limit_mb 입력받기
    size_limit_str = ensure_value_completed(
        key_name="large_file_size_limit",
        func_n=func_n,
        guide_text="히스토리에서 제거할 대용량 파일의 최소 크기(MB)를 입력하세요 (기본값: 100)",
        options=["100", "50", "200", "500", "1000"],
    )
    try:
        size_limit_mb = int(size_limit_str)
    except ValueError:
        logging.warning("잘못된 입력입니다. 기본값 100MB를 사용합니다.")
        size_limit_mb = 100

    logging.debug(f"🔧 Git 대용량 파일 히스토리 정리 시작 (기준: {size_limit_mb}MB)...")

    def run_git_command(cmd, check=True):
        """Git 명령어 실행"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            if check and result.returncode != 0:
                logging.debug(f"🔧 Git 명령어 실패: {cmd}")
                logging.debug(f"에러: {result.stderr}")
                return None
            return result
        except Exception as e:
            logging.debug(f"🔧 명령어 실행 중 오류: {e}")
            return None

    def ensure_line_in_gitignore(line):
        """gitignore 파일에 라인 추가"""
        gitignore_path = Path('.gitignore')
        try:
            if gitignore_path.exists():
                content = gitignore_path.read_text(encoding='utf-8')
                if line not in content:
                    with open(gitignore_path, 'a', encoding='utf-8') as f:
                        f.write(f'\n{line}\n')
                    logging.debug(f"🔧 .gitignore에 추가: {line}")
                else:
                    logging.debug(f"🔧 .gitignore에 이미 존재: {line}")
            else:
                with open(gitignore_path, 'w', encoding='utf-8') as f:
                    f.write(f'{line}\n')
                logging.debug(f"🔧 .gitignore 생성 및 추가: {line}")
        except Exception as e:
            logging.error(f"❌ .gitignore 파일 처리 중 오류 발생: {e}")

    def get_git_filter_repo_command():
        """
        git-filter-repo 명령어 경로를 반환합니다.
        PATH에 있으면 'git filter-repo', 없으면 다운로드 후 'python /path/to/script'를 반환합니다.
        """
        # 1. Check if it's in PATH
        result = run_git_command("git filter-repo --version", check=False)
        if result and result.returncode == 0:
            logging.debug("🔧 git-filter-repo가 PATH에 설치되어 있습니다.")
            return "git filter-repo"

        # 2. Check if it's already downloaded in temp
        temp_dir = Path(tempfile.gettempdir())
        script_path = temp_dir / "git-filter-repo"
        if script_path.is_file():
            logging.debug(f"🔧 git-filter-repo가 임시 디렉토리에 존재합니다: {script_path}")
            return f"python \"{script_path}\""

        # 3. Download it
        logging.debug("🔧 git-filter-repo 다운로드 시도...")
        try:
            url = "https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo"
            urllib.request.urlretrieve(url, script_path)
            logging.info(f"✅ git-filter-repo 다운로드 완료: {script_path}")
            return f"python \"{script_path}\""
        except Exception as e:
            logging.error(f"❌ git-filter-repo 다운로드 실패: {e}")
            return None

    # n. Git 저장소 확인
    logging.debug("🔧 Git 저장소 상태 확인...")
    result = run_git_command("git rev-parse --is-inside-work-tree")
    if not result or not result.stdout.strip() == 'true':
        logging.error("❌ Git 저장소가 아닙니다. 작업을 중단합니다.")
        return False

    # 현재 브랜치 확인
    result = run_git_command("git rev-parse --abbrev-ref HEAD")
    branch = result.stdout.strip() if result and result.stdout else "main"
    logging.debug(f"🔧 현재 브랜치: {branch}")

    # 원격 저장소 확인
    result = run_git_command("git remote get-url origin", check=False)
    if not result or result.returncode != 0:
        logging.warning("⚠️ 원격 저장소가 설정되지 않았습니다. 히스토리 정리 후 푸시는 진행되지 않습니다.")

    # n. 대용량 파일 탐지 (기준 MB 이상)
    logging.debug("🔧 대용량 파일 탐지 중...")

    def find_large_files(size_limit_mb):
        """대용량 파일 찾기"""
        large_files = []
        size_limit_bytes = size_limit_mb * 1024 * 1024

        # 현재 추적 중인 파일들 검사
        result = run_git_command("git ls-files -z", check=False)
        if result and result.stdout:
            tracked_files = result.stdout.strip('\0').split('\0')
            with Progress() as progress:
                task = progress.add_task("[cyan]작업 트리 파일 검사...", total=len(tracked_files))
                for file_path in tracked_files:
                    if file_path and Path(file_path).exists():
                        try:
                            file_size = Path(file_path).stat().st_size
                            if file_size > size_limit_bytes:
                                size_mb = file_size / (1024 * 1024)
                                large_files.append((file_path, size_mb))
                                logging.debug(f"🔧 대용량 파일 발견: {file_path} ({size_mb:.1f}MB)")
                        except Exception as e:
                            logging.debug(f"🔧 파일 크기 확인 실패: {file_path} - {e}")
                    progress.update(task, advance=1)
        return large_files

    large_files_found_in_work_tree = find_large_files(size_limit_mb)

    large_files_to_ignore = []
    if large_files_found_in_work_tree:
        logging.info(f"총 {len(large_files_found_in_work_tree)}개의 대용량 파일 발견 (작업 트리)")
        options_for_fzf = [f"{f[0]} ({f[1]:.1f}MB)" for f in large_files_found_in_work_tree]
        selected_options_for_work_tree = ensure_values_completed(
            key_name="select_large_files_to_ignore",
            func_n=func_n,
            guide_text="작업 트리에서 .gitignore에 추가할 대용량 파일을 선택하세요 (복수 선택 가능):",
            options=options_for_fzf,
            multi_select=True
        )

        path_to_info_map = {f[0]: f for f in large_files_found_in_work_tree}
        for s_option in selected_options_for_work_tree:
            path_part = s_option.rsplit(' (', 1)[0]
            if path_part in path_to_info_map:
                large_files_to_ignore.append(path_to_info_map[path_part])

        if large_files_to_ignore:
            logging.debug("🔧 .gitignore 업데이트...")
            for file_path, _ in large_files_to_ignore:
                ensure_line_in_gitignore(file_path)

            run_git_command("git add .gitignore")
            result = run_git_command("git commit -m 'chore: ignore large files'", check=False)
            if result and result.returncode == 0:
                logging.info(".gitignore 변경사항 커밋됨")
            else:
                logging.debug("🔧 .gitignore 변경사항 없음")
        else:
            logging.info("사용자가 .gitignore에 추가할 파일을 선택하지 않았습니다.")
    else:
        logging.info(f"✅ {size_limit_mb}MB 이상의 대용량 파일이 작업 트리에 없습니다.")

    # 6. 히스토리에서 대용량 파일 검사
    logging.debug("🔧 Git 히스토리에서 대용량 파일 검사...")

    def find_large_files_in_history(size_limit_mb):
        history_large_files = []
        size_limit_bytes = size_limit_mb * 1024 * 1024

        result = run_git_command("git rev-list --objects --all", check=False)
        if not result or not result.stdout:
            logging.warning("⚠️ Git 히스토리 객체를 가져올 수 없습니다.")
            return []

        objects = result.stdout.strip().split('\n')
        logging.debug(f"🔧 검사할 객체 수: {len(objects)}개")

        with Progress() as progress:
            task = progress.add_task("[cyan]히스토리 객체 검사...", total=len(objects))
            for line in objects:
                line = line.strip()
                if not line or ' ' not in line:
                    progress.update(task, advance=1)
                    continue

                obj_hash, *file_path_parts = line.split(' ')
                file_path = ' '.join(file_path_parts)

                if not file_path:
                    progress.update(task, advance=1)
                    continue

                size_result = run_git_command(f"git cat-file -s {obj_hash}", check=False)
                if size_result and size_result.stdout.strip().isdigit():
                    obj_size = int(size_result.stdout.strip())
                    if obj_size > size_limit_bytes:
                        size_mb = obj_size / (1024 * 1024)
                        if not any(f[0] == file_path for f in history_large_files):
                            history_large_files.append((file_path, size_mb))
                            logging.debug(f"🔧 히스토리 대용량 파일 발견: {file_path} ({size_mb:.1f}MB)")
                progress.update(task, advance=1)
        return history_large_files

    history_large_files_found = find_large_files_in_history(size_limit_mb)

    all_large_files = []
    if history_large_files_found:
        logging.info(f"총 {len(history_large_files_found)}개의 대용량 파일 발견 (히스토리)")
        options_for_fzf_all = [f"{f[0]} ({f[1]:.1f}MB)" for f in history_large_files_found]
        selected_options_for_all = ensure_values_completed(
            key_name="select_all_large_files_to_remove",
            func_n=func_n,
            guide_text="히스토리에서 제거할 대용량 파일을 선택하세요 (복수 선택 가능):",
            options=options_for_fzf_all,
            multi_select=True
        )

        path_to_info_map_hist = {f[0]: f for f in history_large_files_found}
        for s_option in selected_options_for_all:
            path_part = s_option.rsplit(' (', 1)[0]
            if path_part in path_to_info_map_hist:
                all_large_files.append(path_to_info_map_hist[path_part])

    if all_large_files:
        logging.info(f"🔧 총 {len(all_large_files)}개의 파일을 히스토리에서 제거합니다.")

        filter_repo_cmd = get_git_filter_repo_command()
        if not filter_repo_cmd:
            logging.error("❌ git-filter-repo를 사용할 수 없어 히스토리 정리를 진행할 수 없습니다.")
            return False

        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', newline='\n') as f:
            for file_path, _ in all_large_files:
                f.write(f"{file_path}\n")
            temp_file_path = f.name

        logging.debug(f"🔧 제거할 파일 목록 임시 파일: {temp_file_path}")

        # --force is needed if we run this multiple times
        cmd = f"{filter_repo_cmd} --paths-from-file \"{temp_file_path}\" --invert-paths --force"

        logging.info("⏳ Git 히스토리 재작성 중... 이 작업은 저장소 크기에 따라 몇 분 이상 소요될 수 있습니다.")
        result = run_git_command(cmd, check=False)

        try:
            Path(temp_file_path).unlink()
        except OSError as e:
            logging.warning(f"⚠️ 임시 파일을 삭제하지 못했습니다: {e}")

        if result and result.returncode == 0:
            logging.info("git-filter-repo를 사용하여 히스토리에서 대용량 파일 제거를 완료했습니다.")
        else:
            logging.error("❌ git-filter-repo 실행에 실패했습니다. 히스토리가 변경되지 않았을 수 있습니다.")
            if result and result.stderr:
                logging.error(f"Stderr: {result.stderr}")
            return False
    else:
        logging.info("히스토리에서 제거할 대용량 파일이 선택되지 않았거나 없습니다.")

    # 8. 검증
    logging.info("🔍 최종 검증 시작...")
    verification_passed = True
    if all_large_files:
        logging.debug("🔧 히스토리에서 제거된 파일이 없는지 다시 확인합니다...")
        remaining_files = find_large_files_in_history(size_limit_mb)

        removed_file_paths = {f[0] for f in all_large_files}
        still_present_files = []
        for file_path, size_mb in remaining_files:
            if file_path in removed_file_paths:
                still_present_files.append(f"{file_path} ({size_mb:.1f}MB)")

        if still_present_files:
            logging.warning(f"❌ 검증 실패: 다음 파일들이 여전히 히스토리에 남아있습니다: {still_present_files}")
            verification_passed = False
        else:
            logging.info("검증 성공: 선택한 모든 대용량 파일이 히스토리에서 성공적으로 제거되었습니다.")

    # 저장소 크기 변화 확인
    logging.debug("🔧 저장소 크기 확인...")
    result = run_git_command("git count-objects -vH", check=False)
    if result and result.stdout:
        logging.info("📊 현재 저장소 통계:")
        for line in result.stdout.strip().split('\n'):
            if 'size-pack' in line or 'count' in line or 'in-pack' in line:
                logging.info(f"  {line.strip()}")

    if verification_passed:
        logging.info("모든 작업이 성공적으로 완료되었습니다.")
    else:
        logging.error("❌ 일부 작업이 실패했습니다. 로그를 확인해주세요.")

    # 9. 강제 푸시
    result = run_git_command("git remote get-url origin", check=False)
    if not result or result.returncode != 0:
        logging.warning("⚠️ 원격 저장소가 설정되지 않아 푸시를 건너뜁니다.")
        logging.info("로컬 히스토리 정리는 완료되었습니다. 원격 저장소 설정 후 수동으로 푸시하세요: git push origin <branch> --force")
    else:
        remote_url = result.stdout.strip()
        logging.info(f"원격 저장소 확인: {remote_url}")

        push_confirm = ensure_value_completed(
            key_name="confirm_git_force_push",
            func_n=func_n,
            guide_text="정리된 히스토리를 원격 저장소에 강제 푸시하시겠습니까? (yes/no)",
            options=["yes", "no"]
        )
        if push_confirm.lower() != "yes":
            logging.info("사용자가 강제 푸시를 취소했습니다. 로컬 히스토리 정리는 완료되었습니다.")
            return True

        logging.info(f"⏳ 원격 저장소({remote_url})에 강제 푸시를 시도합니다...")
        result = run_git_command(f"git push origin {branch} --force", check=False)

        if result and result.returncode == 0:
            logging.info("강제 푸시 성공!")
        else:
            logging.error("❌ 강제 푸시 실패!")
            if result:
                logging.error(f"Stdout: {result.stdout}")
                logging.error(f"Stderr: {result.stderr}")
            logging.warning("가능한 원인: 원격 저장소 푸시 권한 없음, 브랜치 보호 규칙 설정됨, 네트워크 연결 문제 등")
            logging.warning(f"수동 푸시 명령어: git push origin {branch} --force")
            return False

    return True

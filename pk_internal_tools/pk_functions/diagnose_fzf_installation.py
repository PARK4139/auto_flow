from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def diagnose_fzf_installation():
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_colors import PkColors

    """fzf 설치 상태를 진단합니다."""
    try:
        try:
            pass
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'FZF_DIAGNOSIS_START': 'fzf 설치 상태를 진단합니다',
                'FZF_FOUND': 'fzf 발견',
                'FZF_NOT_FOUND': 'fzf를 찾을 수 없음',
                'FZF_EXE_FOUND': 'fzf.exe 발견',
                'FZF_EXE_NOT_FOUND': 'fzf.exe를 찾을 수 없음',
                'FZF_PATH_FOUND': '발견',
                'FZF_PATH_NOT_FOUND': '없음',
                'FZF_EXECUTION_SUCCESS': '실행 성공',
                'FZF_EXECUTION_FAILED': '실행 실패',
                'FZF_CORRUPTED_FILE': '손상된 파일',
                'FZF_OS_ERROR': 'OS 오류',
                'FZF_FILE_NOT_FOUND': '파일 없음',
                'FZF_OTHER_ERROR': '기타 오류',
                'FZF_AVAILABLE': '사용 가능한 fzf',
                'FZF_NOT_AVAILABLE': '사용 가능한 fzf가 없습니다'
            })()

        print("fzf 설치 상태를 진단합니다...")

        # n. 시스템 PATH에서 fzf 검색
        import shutil
        fzf_path = shutil.which("fzf")
        if fzf_path:
            logging.debug(f"[{PkTexts.FZF_FOUND}] {PkColors.CYAN}경로={fzf_path} {PkColors.RESET}")
        else:
            logging.debug(f"[{PkTexts.FZF_NOT_FOUND}]")

        # n. Windows에서 fzf.exe 검색
        from pk_internal_tools.pk_objects.pk_files import F_FZF
        f_fzf: Path = F_FZF
        if f_fzf.exists():
            logging.debug(f"[{PkTexts.FZF_EXE_FOUND}] {PkColors.CYAN}경로={f_fzf} {PkColors.RESET}")
        else:
            logging.debug(f"[{PkTexts.FZF_EXE_NOT_FOUND}]")

        # n. 일반적인 설치 경로 확인
        common_paths = [
            "/usr/bin/fzf",
            "/usr/local/bin/fzf",
            "/opt/homebrew/bin/fzf",
            str(Path.home() / "fzf.exe"),
            str(Path.home() / ".local/bin/fzf"),
            str(Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Junegunn.fzf_Microsoft.Winget.Source_8wekyb3d8bbwe/fzf.exe")
        ]

        found_paths = []
        for path in common_paths:
            if Path(path).exists():
                found_paths.append(path)
                logging.debug(f"[{PkTexts.FZF_PATH_FOUND}] {PkColors.CYAN}경로={path} {PkColors.RESET}")
            else:
                logging.debug(f"[{PkTexts.FZF_PATH_NOT_FOUND}] {PkColors.GREY}경로={path} {PkColors.RESET}")

        # n. 실행 테스트
        working_fzf = None
        test_paths = [fzf_path] + found_paths if fzf_path else found_paths

        for path in test_paths:
            if not path:
                continue

            try:
                import subprocess
                result = subprocess.run([path, "--version"],
                                        capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logging.debug(f"[{PkTexts.FZF_EXECUTION_SUCCESS}] {PkColors.CYAN}경로={path} {PkColors.RESET}")
                    working_fzf = path
                    break
                else:
                    logging.debug(f"[{PkTexts.FZF_EXECUTION_FAILED}] {PkColors.RED}경로={path} 오류코드={result.returncode} {PkColors.RESET}")

            except subprocess.TimeoutExpired:
                logging.debug(f"[{PkTexts.FZF_EXECUTION_FAILED}] {PkColors.RED}경로={path} 타임아웃 {PkColors.RESET}")
            except FileNotFoundError:
                logging.debug(f"[{PkTexts.FZF_FILE_NOT_FOUND}] {PkColors.RED}경로={path} {PkColors.RESET}")
            except PermissionError:
                logging.debug(f"[{PkTexts.FZF_OS_ERROR}] {PkColors.RED}경로={path} 권한오류 {PkColors.RESET}")
            except Exception as e:
                logging.debug(f"[{PkTexts.FZF_OTHER_ERROR}] {PkColors.RED}경로={path} 오류={e} {PkColors.RESET}")

        # n. 결과 요약
        if working_fzf:
            logging.debug(f"[{PkTexts.FZF_AVAILABLE}] {PkColors.CYAN}경로={working_fzf} {PkColors.RESET}")
            return working_fzf
        else:
            logging.debug(f"[{PkTexts.FZF_NOT_AVAILABLE}]")
            return None

    except Exception as e:
        logging.debug(f"[{PkTexts.FZF_OTHER_ERROR}] {PkColors.RED}오류={e} {PkColors.RESET}")
        return None


if __name__ == "__main__":
    diagnose_fzf_installation()

import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def _get_path_size(path: Path) -> int:
    """
    주어진 경로(파일 또는 디렉토리)의 크기를 바이트 단위로 반환합니다.
    디렉토리인 경우 모든 하위 파일의 크기를 합산합니다.
    """
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        total_size = 0
        for entry in path.rglob('*'):
            if entry.is_file():
                total_size += entry.stat().st_size
        return total_size
    return 0


def _format_size(size_in_bytes: int) -> str:
    """
    바이트 크기를 사람이 읽기 쉬운 형식(KB, MB, GB)으로 변환합니다.
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"


@ensure_seconds_measured
def ensure_recycle_bin_empty_permanently():
    """
        # TODO 삭제할 pnx 사용자에게 보여줄때, size 에 따라서 내림차순 정렬되도록
    """
    import logging
    import platform
    import shutil
    import sys
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_directories import D_RECYCLE_BIN_C, D_RECYCLE_BIN_D
    from pk_internal_tools.pk_objects.pk_directories import D_RECYCLE_BIN_G

    try:
        """
        사용자에게 휴지통 내용을 보여주고, 선택된 항목을 영구적으로 삭제합니다.
        """
        func_n = get_caller_name()

        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}휴지통 비우기 도구 시작{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

        if platform.system().lower() != "windows":
            logging.error("이 스크립트는 Windows 운영체제에서만 동작합니다.")
            return

        # 전체 Windows 휴지통 비우기 옵션
        clear_all_option = f"전체 Windows 휴지통 비우기 (모든 드라이브)"

        # 기존 드라이브별 휴지통 경로 수집
        drive_recycle_bin_options = []
        recycle_bin_paths = []
        if D_RECYCLE_BIN_C.exists():
            recycle_bin_paths.append(D_RECYCLE_BIN_C)
            drive_recycle_bin_options.append(f"{str(D_RECYCLE_BIN_C)} (C 드라이브)")
        if D_RECYCLE_BIN_D.exists():
            recycle_bin_paths.append(D_RECYCLE_BIN_D)
            drive_recycle_bin_options.append(f"{str(D_RECYCLE_BIN_D)} (D 드라이브)")
        if D_RECYCLE_BIN_G.exists():
            recycle_bin_paths.append(D_RECYCLE_BIN_G)
            drive_recycle_bin_options.append(f"{str(D_RECYCLE_BIN_G)} (G 드라이브)")

        # 사용자에게 비울 휴지통 드라이브 또는 전체 비우기 선택 옵션 제공
        options = [clear_all_option] + drive_recycle_bin_options

        if not options:
            logging.warning(f"비울 수 있는 휴지통 경로를 찾을 수 없습니다")
            return

        selected_option = ensure_value_completed(
            key_name=f"d_working_recycle_bin_selection",
            func_n=func_n,
            guide_text="비울 휴지통 옵션을 선택하세요:",
            options=options
        )

        if not selected_option:
            logging.info(f"휴지통 비우기 선택을 취소했습니다")
            return

        if selected_option == clear_all_option:
            logging.info(f"{PkColors.RED}전체 Windows 휴지통을 비웁니다...{PkColors.RESET}")
            from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
            from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui  # Add this import
            try:
                # PowerShell 명령을 사용하여 Windows 휴지통 비우기
                cmd = "powershell.exe -Command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\""
                ensure_command_executed(cmd=cmd)
                logging.info(f"{PkColors.TC_ORANGE_TONE1}전체 Windows 휴지통 비우기 완료.{PkColors.RESET}")
                # alert_as_gui("전체 Windows 휴지통 비우기 완료.")
                return True  # 전체 휴지통 비우기 완료 후 함수 종료
            except Exception as e:
                logging.error(f"전체 Windows 휴지통 비우기 중 오류 발생: {e}")
                return False

        # 이하 기존 드라이브별 휴지통 내용 삭제 로직
        target_recycle_bin = Path(selected_option.split(' ')[0])  # 선택된 드라이브 경로만 추출

        if not recycle_bin_paths:
            logging.info(f"{PkColors.YELLOW}감지된 휴지통 경로가 없습니다.{PkColors.RESET}")
            logging.info(f"{PkColors.YELLOW}D_RECYCLE_BIN_C: {D_RECYCLE_BIN_C.exists()}{PkColors.RESET}")
            logging.info(f"{PkColors.YELLOW}D_RECYCLE_BIN_D: {D_RECYCLE_BIN_D.exists()}{PkColors.RESET}")
            if hasattr(sys.modules[__name__], 'D_RECYCLE_BIN_G'):
                logging.info(f"{PkColors.YELLOW}D_RECYCLE_BIN_G: {D_RECYCLE_BIN_G.exists()}{PkColors.RESET}")
            else:
                logging.info(f"{PkColors.YELLOW}D_RECYCLE_BIN_G 정의되지 않음{PkColors.RESET}")
            return

        d_working_recycle_bin = ensure_value_completed(
            key_name=f"d_working_recycle_bin",
            func_n=func_n,
            guide_text="비울 휴지통 드라이브를 선택하세요:",
            options=[str(p) for p in recycle_bin_paths]
        )

        if not d_working_recycle_bin:
            logging.info(f"{PkColors.YELLOW}휴지통 드라이브 선택을 취소했습니다.{PkColors.RESET}")
            return

        target_recycle_bin = Path(d_working_recycle_bin)

        items_to_delete_options = []
        item_paths = []

        # 현재 휴지통 경로 내의 실제 삭제 항목 ($R... 형식의 파일 또는 폴더)을 확인
        for item_path in target_recycle_bin.iterdir():
            if item_path.name.startswith('$R'):  # 파일과 폴더 모두 $R로 시작할 수 있음
                try:
                    size = _get_path_size(item_path)
                    formatted_size = _format_size(size)
                    # 여기서는 임시로 $R... 파일/폴더 이름과 경로를 표시
                    items_to_delete_options.append(f"({formatted_size}) {item_path.name} - {target_recycle_bin.name}")
                    item_paths.append(item_path)
                except Exception as e:
                    logging.warning(f"항목 크기 계산 중 오류 발생: {item_path} - {e}")
            elif item_path.is_file() and item_path.name.startswith('$I'):
                # $I 파일은 나중에 파싱하여 원래 파일 이름을 가져올 예정 (현재는 무시)
                pass

        if not items_to_delete_options:
            logging.info(f"{PkColors.YELLOW}선택된 휴지통 '{target_recycle_bin}'에 비울 항목이 없습니다.{PkColors.RESET}")
            return

        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}선택된 휴지통 '{target_recycle_bin}'의 내용:{PkColors.RESET}")
        for i, option in enumerate(items_to_delete_options):
            logging.info(f" {i + 1}. {option}")
        logging.info(PK_UNDERLINE)

        pnx_to_delete = ensure_values_completed(
            key_name=f"pnx_to_delete",
            options=items_to_delete_options,
            func_n=func_n,
            guide_text="삭제하면 되돌릴 수 없습니다. 충분히 고려후 선택하세요",
        )
        # ok = ensure_values_completed(
        #     key_name=f"r u sure",
        #     func_n=func_n,
        #     guide_text="정말로 삭제할까요?",
        #     options=[PkTexts.YES, PkTexts.NO],
        # )
        # if not ok:
        #     logging.info(rf"삭제 취소")
        #     return
        if not pnx_to_delete:
            logging.info(f"{PkColors.YELLOW}선택된 항목이 없어 삭제를 취소합니다.{PkColors.RESET}")
            return

        logging.info(f"{PkColors.TC_ORANGE_TONE1}다음 항목들을 영구적으로 삭제합니다:{PkColors.RESET}")
        paths_to_remove = []
        for option_str in pnx_to_delete:
            try:
                index = items_to_delete_options.index(option_str)
                paths_to_remove.append(item_paths[index])
                logging.info(f"{item_paths[index]}")
            except ValueError:
                logging.error(f"선택된 옵션 '{option_str}'에 해당하는 경로를 찾을 수 없습니다. (내부 오류)")
                continue

        if not paths_to_remove:
            logging.info(f"{PkColors.YELLOW}삭제할 유효한 경로가 없어 작업을 종료합니다.{PkColors.RESET}")
            return

        ok = ensure_value_completed(
            key_name="delete_confirm",
            func_n=func_n,
            guide_text=f"{PkColors.RED}경고: 선택된 항목들은 영구적으로 삭제됩니다. 계속하시겠습니까? (yes/no){PkColors.RESET}",
            options=["yes", "no"]
        )
        if ok.lower() != "yes":
            logging.info(f"{PkColors.YELLOW}사용자가 삭제를 취소했습니다.{PkColors.RESET}")
            return

        for path in paths_to_remove:
            try:
                if path.is_file():
                    path.unlink()  # 파일 삭제
                    logging.info(f"파일 삭제 완료: {path}")
                elif path.is_dir():
                    shutil.rmtree(path)  # 디렉토리 및 내용물 삭제
                    logging.info(f"디렉토리 삭제 완료: {path}")
                else:
                    logging.warning(f"알 수 없는 유형의 경로입니다 (건너뛰기): {path}")
            except OSError as e:
                logging.error(f"경로 삭제 중 오류 발생 {path}: {e}")
            except Exception as e:
                logging.error(f"예기치 않은 오류로 삭제 실패 {path}: {e}", exc_info=True)
        logging.info(f"{PkColors.TC_ORANGE_TONE1}휴지통 비우기 작업 완료.{PkColors.RESET}")

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        # cleanup (e.g. stop_live_display in other contexts)
        pass

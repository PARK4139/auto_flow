from pathlib import Path
from typing import Union, Optional
import subprocess
import shlex
import shutil
from datetime import datetime
import logging
import traceback
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE # Import QC_MODE

EXCLUDES = [
    "-x*.venv/*",
    "-x*.venv/*",
    "-x*.venv/*",
    "-x.idea/*",
    "-x.vscode/*",
    "-x.git/*",
    "-x.github/*",
]

def _ts() -> str:
    # 고정 포맷: _YYYY_MMDD_HHMM
    return datetime.now().strftime("_%Y_%m%d_%H%M")


def ensure_pnx_compressed_via_rar(
    pnx: Union[str, Path],
    d_dst: Union[str, Path],
    with_timestamp:bool = True,
) -> Optional[Path]:
    """
    주어진 디렉터리/파일(pnx)을 WSL rar로 .rar 아카이브 생성 후
    d_dst에 최종 산출물(.rar)을 배치한다.
    """
    try:
        # 입력 정규화
        pnx = Path(pnx)
        d_dst = Path(d_dst)
        d_dst.mkdir(parents=True, exist_ok=True)

        if QC_MODE: # If in test environment, create a zip file
            logging.debug(f"[ensure_pnx_compressed_via_rar] QC_MODE is True. Creating ZIP archive.")
            base_name = pnx.name if pnx.is_dir() else pnx.stem
            archive_name = f"{base_name}{_ts()}" if with_timestamp else base_name
            
            # shutil.make_archive creates a .zip file by default
            # It returns the path to the archive without the extension
            archive_path = shutil.make_archive(
                base_name=str(d_dst / archive_name),
                format='zip',
                root_dir=pnx.parent if pnx.is_file() else pnx,
                base_dir=pnx.name if pnx.is_file() else None
            )
            final_archive_path = Path(archive_path) # Removed the extra .zip
            logging.info(f"ZIP archive ready: {final_archive_path}")
            return final_archive_path

        # Original logic for RAR creation (when QC_MODE is False)
        # 산출물(작업용) 경로 설정
        drive_letter = pnx.drive[0].lower()
        # Convert Windows path to WSL path
        def to_wsl_path(win_path: Path) -> Path:
            return Path(f"/mnt/{win_path.drive[0].lower()}/{win_path.as_posix()[3:]}")

        pnx_wsl = to_wsl_path(pnx)
        target_dir_wsl = pnx_wsl if pnx.is_dir() else pnx_wsl.parent

        # 작업용 RAR 파일 경로 (Windows/WSL)
        f_rar_win = pnx.parent / f"{pnx.name}.rar" if pnx.is_dir() else pnx.parent / f"{pnx.stem}.rar"
        f_rar_wsl = to_wsl_path(f_rar_win)

        logging.debug(f"LOCK pnx_win={pnx}")
        logging.debug(f"LOCK target_dir_wsl={target_dir_wsl}")
        logging.debug(f"LOCK wsl_f_rar={f_rar_wsl}")

        # n. RAR 생성
        cmd_args = ["wsl", "--", "rar", "a", f_rar_wsl.as_posix()] + EXCLUDES
        # 디렉터리 전체를 포장하려면 뒤에 대상 디렉터리를 명시
        # (파일 하나면 그 파일을 명시)
        if pnx.is_dir():
            cmd_args.append(target_dir_wsl.as_posix())
        else:
            cmd_args.append(pnx_wsl.as_posix())

        logging.debug(f"cmd_args={cmd_args}")
        proc = subprocess.run(" ".join(shlex.quote(arg) for arg in cmd_args), capture_output=True, text=True, shell=True)
        if proc.returncode != 0:
            logging.error(f"RAR create failed: rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}")
            return None

        # 2) 생성 검증
        if not f_rar_win.exists():
            logging.error(f"RAR not found after creation: {f_rar_win}")
            return None

        # 3) 결과 파일명 결정 (타임스탬프 적용)
        base_name = pnx.name if pnx.is_dir() else pnx.stem
        suffix = _ts() if with_timestamp else ""
        f_rar_final = d_dst / f"{base_name}{suffix}.rar"

        # 덮어쓰지 않기 위해 기존 파일 제거 또는 시퀀셜 처리 등 정책 적용 가능
        if f_rar_final.exists():
            # 여기서는 간단히 시퀀셜 처리
            for i in range(1, 1000):
                candidate = d_dst / f"{base_name}{suffix}({i}).rar"
                if not candidate.exists():
                    f_rar_final = candidate
                    break

        # 4) 산출물 배치: 복사(copy2) 후 필요 시 작업용 파일 삭제
        shutil.copy2(f_rar_win, f_rar_final)

        # 5) 최종 검증
        if not f_rar_final.exists():
            logging.error(f"Final archive missing: {f_rar_final}")
            return None

        logging.info(f"RAR archive ready: {f_rar_final}")
        return f_rar_final
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return None # Return None on error
import logging
import subprocess

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed  # Existing fallback
from pk_internal_tools.pk_functions.get_fzf_executable_command import get_fzf_executable_command  # New import
from pk_internal_tools.pk_objects.pk_etc import PK_POINTER_COLOR, PK_PROMPT_COLOR, PK_HL_COLOR, PK_HL_ACTIVE_COLOR, PK_FG_ACTIVE_COLOR, PK_QUERY_COLOR, PK_POINTER_TEXT, PK_SPINNER_COLOR


def ensure_values_completed_2025_10_23(key_name: str, options: list[str], multi_select: bool = False) -> list[str]:
    """
    fzf 외부 명령어를 사용하여 사용자에게 다중 선택 가능한 목록을 제시하고,
    선택된 값들을 리스트로 반환합니다.
    multi_select가 False인 경우 단일 선택 모드로 동작합니다.
    """
    if not options:
        return []

    fzf_executable_command = get_fzf_executable_command()
    if not fzf_executable_command:
        logging.error("fzf 명령어를 찾을 수 없습니다. fzf가 설치되어 있고 PATH에 있는지 확인해주세요.")
        logging.warning("fzf를 찾을 수 없어 단일 선택 모드로 대체합니다.")
        # Fallback to the project-specific single-select function
        selected = ensure_value_completed(key_name=key_name, options=options)
        return [selected] if selected else []

    try:
        fzf_args = [
            str(fzf_executable_command),  # Use the found executable path
            "--ansi",
            "--prompt", f"{key_name}> ",
            "--print0",
            f"--pointer={PK_POINTER_TEXT}",
            f"--color=query:{PK_QUERY_COLOR},spinner:{PK_SPINNER_COLOR},prompt:{PK_PROMPT_COLOR},pointer:{PK_POINTER_COLOR},hl:{PK_HL_COLOR},hl+:{PK_HL_ACTIVE_COLOR},fg+:{PK_FG_ACTIVE_COLOR}",
            "--height=40%",  # Common design pattern
            "--layout=reverse",  # Common design pattern
            "--border",  # Common design pattern
        ]
        if multi_select:
            fzf_args.insert(1, "--multi")  # Insert --multi after fzf_executable_command

        # 더블클릭으로 클립보드에 복사 (Windows)
        import platform
        if platform.system() == "Windows":
            # Windows: clip.exe 사용
            fzf_args.append("--bind")
            fzf_args.append("double-click:execute-silent(echo {} | clip.exe)")
        else:
            # Linux/Mac: xclip 또는 pbcopy 사용
            fzf_args.append("--bind")
            fzf_args.append("double-click:execute-silent(echo {} | xclip -selection clipboard 2>/dev/null || echo {} | pbcopy 2>/dev/null || true)")

        process = subprocess.run(
            fzf_args,
            input='\n'.join(options).encode('utf-8'),
            capture_output=True,
            check=True
        )

        selected_values = process.stdout.decode('utf-8').strip('\0').split('\0')

        return [v for v in selected_values if v]

    except subprocess.CalledProcessError as e:
        if e.returncode == 130:  # User cancelled (Ctrl+C or ESC)
            logging.info("fzf 선택이 사용자에 의해 취소되었습니다.")
            return []
        logging.error(f"fzf 실행 중 오류 발생 (코드: {e.returncode}): {e.stderr.decode('utf-8')}")
        return []
    except Exception as e:
        logging.error(f"fzf 다중 선택 처리 중 예상치 못한 오류 발생: {e}")
        return []

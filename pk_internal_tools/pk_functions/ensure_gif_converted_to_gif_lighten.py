import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_n import get_n


@ensure_seconds_measured
def ensure_gif_converted_to_gif_lighten(
        input_file_path: Path = None,
        output_file_name: str = None,
        start_time: str = None,
        duration: str = None,
        fps: str = None,
        scale: str = None,
        loop: str = None,
) -> bool:
    """
        TODO: Write docstring for ensure_gif_converted_to_gif_lighten.
    """
    try:

        """
        FFmpeg를 사용하여 GIF 파일을 변환하는 래퍼 함수입니다.
        사용자로부터 필요한 인자를 입력받아 GIF 변환 명령을 실행합니다.

        Args:
            input_file_path (Path, optional): 입력 GIF 파일 경로. Defaults to None.
            output_file_name (str, optional): 출력 GIF 파일 이름. Defaults to None.
            start_time (str, optional): 시작 시간 (초). Defaults to None.
            duration (str, optional): 재생 시간 (초). Defaults to None.
            fps (str, optional): 초당 프레임 수. Defaults to None.
            scale (str, optional): 스케일 설정. Defaults to None.
            loop (str, optional): 루프 횟수 (0 = 무한). Defaults to None.

        Returns:
            bool: GIF 변환 성공 여부.
        """
        import logging
        import textwrap
        from pathlib import Path

        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_colors import PkColors
        from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

        func_n = get_caller_name()
        logging.info(f"{PkColors.BRIGHT_CYAN}FFmpeg GIF 변환 시작{PkColors.RESET}")

        # ensure_value_completed를 사용하여 인자 받기
        input_file_path_str = ensure_value_completed(
            key_name=f"{func_n}_input_file_path",
            func_n=func_n,
            guide_text="변환할 GIF 파일의 절대 경로를 입력하세요:",
            options=[]
        )
        input_file_path = Path(input_file_path_str)

        output_file_name = ensure_value_completed(
            key_name=f"{func_n}_output_file_name",
            func_n=func_n,
            guide_text="출력될 GIF 파일의 이름을 입력하세요 (예: output.gif):",
            options=[rf"{get_n(input_file_path)}_lighten.gif"]
        )

        start_time = ensure_value_completed(
            key_name=f"{func_n}_start_time",
            func_n=func_n,
            guide_text="시작 시간 (초, 예: 0):",
            options=["0"]
        )

        duration = ensure_value_completed(
            key_name=f"{func_n}_duration",
            func_n=func_n,
            guide_text="재생 시간 (초, 예: 8):",
            options=["8"]
        )

        fps = ensure_value_completed(
            key_name=f"{func_n}_fps",
            func_n=func_n,
            guide_text="초당 프레임 수 (fps, 예: 12):",
            options=["12"]
        )

        scale = ensure_value_completed(
            key_name=f"{func_n}_scale",
            func_n=func_n,
            guide_text="스케일 (예: 800:-1):",
            options=["800:-1"]
        )

        loop = ensure_value_completed(
            key_name=f"{func_n}_loop",
            func_n=func_n,
            guide_text="루프 횟수 (0 = 무한, 예: 0):",
            options=['0']
        )
        ffmpeg_exe_path = F_FFMPEG_EXE
        if not ffmpeg_exe_path.exists():
            logging.error(f"FFmpeg 실행 파일을 찾을 수 없습니다: {ffmpeg_exe_path}")
            return False

        # 임시 출력 디렉토리 (input_file_path와 동일한 디렉토리에 저장하도록 함)
        output_dir = input_file_path.parent
        output_file_path = output_dir / output_file_name

        command = textwrap.dedent(f'''
            "{ffmpeg_exe_path}" -i "{input_file_path}" -ss {start_time} -t {duration} -vf "fps={fps},scale={scale}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop {loop} "{output_file_path}"
        ''').strip()

        logging.info(f"실행할 FFmpeg 명령어:\n{command}")

        try:
            ensure_command_executed(command)
            logging.info(f"GIF 변환 완료: {output_file_path}")
            ensure_pnx_opened_by_ext(output_dir)
            return True
        except Exception as e:
            logging.error(f"FFmpeg 명령어 실행 중 오류 발생: {e}")
            return False
        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass

import traceback
import logging
from pathlib import Path
from typing import Optional

# Lazy import for argparse
try:
    import argparse
except ImportError:
    pass

    # Lazy import for project-specific utilities
try:
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
    from pk_internal_tools.pk_web_server.pk_functions.ensure_pk_web_server_run import ensure_pk_web_server_run, app # Import 'app'
    from pk_internal_tools.pk_functions.ensure_remote_command_executed import ensure_remote_command_executed
    from pk_internal_tools.pk_objects.pk_colorful_logging_formatter import PK_UNDERLINE
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForEnsurePkWebServerExecuted
    from pk_internal_tools.pk_functions.get_pk_fzf_options import get_pk_fzf_options # Not used in final, but kept for context if needed later
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
except ImportError as e:
    logging.error(f"Failed to import project utilities: {e}")
    # Fallback/exit strategy if core utilities cannot be imported
    exit(1)

# Lazy import for uvicorn
try:
    import uvicorn
except ImportError:
    uvicorn = None

def main():
    """
    PK 웹 서버를 실행하는 래퍼 스크립트입니다.
    명령줄 인자를 파싱하여 웹 서버 실행 함수를 호출하거나 원격 명령을 실행합니다.
    """
    func_n = Path(__file__).stem
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)

    parser = argparse.ArgumentParser(description="PK 웹 서버를 실행합니다.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="서버가 수신 대기할 호스트 주소")
    parser.add_argument("--port", type=int, default=8000, help="서버가 수신 대기할 포트 번호")
    parser.add_argument("--remote_target", type=str, default=None,
                        help="서버를 실행할 원격 대상의 주소 (예: user@host). None이면 로컬에서 실행됩니다.")
    
    # fzf를 통한 옵션 선택을 위한 인자 추가
    parser.add_argument("--select-option", action="store_true", help="fzf를 사용하여 추가 옵션 선택")

    args = parser.parse_args()

    host = args.host
    port = args.port
    remote_target = args.remote_target

    # fzf를 통한 옵션 선택 로직
    if args.select_option:
        options = [member.value.lower() for member in SetupOpsForEnsurePkWebServerExecuted]
        guide_text = "PK 웹 서버 실행 옵션을 선택하세요:"
        selected_option_str = ensure_value_completed(
            key_name=f"{func_n}_select_option",
            func_n=func_n,
            options=options,
            guide_text=guide_text
        )

        if selected_option_str == SetupOpsForEnsurePkWebServerExecuted.HOST.value.lower():
            host = ensure_value_completed(
                key_name=f"{func_n}_host",
                func_n=func_n,
                guide_text="호스트 주소를 입력하세요 (기본값: 0.0.0.0):",
                default_value=host
            )
        elif selected_option_str == SetupOpsForEnsurePkWebServerExecuted.PORT.value.lower():
            port_str = ensure_value_completed(
                key_name=f"{func_n}_port",
                func_n=func_n,
                guide_text="포트 번호를 입력하세요 (기본값: 8000):",
                default_value=str(port)
            )
            try:
                port = int(port_str)
            except ValueError:
                logging.error(f"{PkColors.RED}유효하지 않은 포트 번호입니다. 기본값 8000을 사용합니다.{PkColors.RESET}")
                port = 8000
        elif selected_option_str == SetupOpsForEnsurePkWebServerExecuted.REMOTE_TARGET.value.lower():
            remote_target = ensure_value_completed(
                key_name=f"{func_n}_remote_target",
                func_n=func_n,
                guide_text="원격 대상 주소를 입력하세요 (예: user@host):",
                default_value=""
            )
            if not remote_target:
                remote_target = None # 빈 문자열이면 None으로 처리

    try:
        ensure_pk_web_server_run(host=host, port=port, remote_target=remote_target)
        
        if remote_target:
            if uvicorn is not None:
                logging.warning(f"{PkColors.YELLOW}원격 대상이 지정되었으므로 로컬 Uvicorn 실행을 건너뜝니다.{PkColors.RESET}")
            
            project_root = Path(__file__).resolve().parent.parent.parent
            # Assuming the remote system has Python and uvicorn installed
            # and the project structure is mirrored or the path is adjusted.
            # For simplicity, we'll assume pk_system is also in the home directory
            # or a similar accessible path on the remote.
            
            # Construct the path to the ensure_pk_web_server_run module on the remote
            # This path needs to be relative to the remote's PYTHONPATH or explicit.
            # Example: ~/pk_system/pk_internal_tools/pk_web_server/pk_functions/ensure_pk_web_server_run.py
            # For now, let's assume direct execution in the remote project root
            # or that the remote Python environment is set up to find the module.
            # A more robust solution might involve copying files or managing remote PYTHONPATH.
            remote_module_path = "pk_internal_tools.pk_web_server.pk_functions.ensure_pk_web_server_run"
            
            remote_command = f"python -m uvicorn {remote_module_path}:app --host {host} --port {port}"
            logging.info(f"{PkColors.BRIGHT_MAGENTA}원격에서 웹 서버 실행 시도 중: {remote_target}{PkColors.RESET}")
            logging.info(f"원격 명령: {remote_command}")
            
            exit_code, stdout, stderr = ensure_remote_command_executed(
                remote_target=remote_target,
                command=remote_command,
                check=False # Do not raise exception for non-zero exit code here, handle it below
            )
            
            if exit_code != 0:
                logging.error(f"{PkColors.RED}원격 웹 서버 실행 실패!{PkColors.RESET}")
                if stdout: logging.error(f"STDOUT:\n{stdout}")
                if stderr: logging.error(f"STDERR:\n{stderr}")
            else:
                logging.info(f"{PkColors.GREEN']}원격 웹 서버 실행 명령 성공! 원격 서버의 로그를 확인하세요.{PkColors.RESET}")
        else:
            # Local execution
            if uvicorn is None:
                logging.error(f"{PkColors.RED}Uvicorn이 설치되어 있지 않습니다. 로컬에서 서버를 실행할 수 없습니다.{PkColors.RESET}")
                logging.info(f"{PkColors.BRIGHT_YELLOW}uv add 'uvicorn'을 실행하여 설치하십시오.{PkColors.RESET}")
                return

            logging.info(f"{PkColors.BRIGHT_GREEN}로컬 웹 서버 시작 중: http://{host}:{port}{PkColors.RESET}")
            uvicorn.run(app, host=host, port=port)

    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)
    finally:
        # 이전에 언급된 pk_ensure_gemini_cli_worked_done.py 실행은
        # 이 래퍼 스크립트를 호출하는 상위 프로세스에서 담당하도록 합니다.
        # 래퍼 스크립트 자체는 단일 작업을 수행하고 종료해야 합니다.
        logging.info(PK_UNDERLINE)
        logging.info("PK 웹 서버 실행 래퍼 스크립트가 완료되었습니다.")
        logging.info(PK_UNDERLINE)

if __name__ == "__main__":
    main()

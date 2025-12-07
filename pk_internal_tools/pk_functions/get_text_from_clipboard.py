def get_text_from_clipboard():
    import logging
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    if is_os_windows():
        # n. stdout과 stderr를 분리해서 받습니다.
        stdout_lines, stderr_lines, _ = ensure_command_executed('powershell.exe Get-Clipboard')

        if stderr_lines:
            logging.error(f"클립보드 읽기 실패: {stderr_lines}")
            return "" # 에러 발생 시 빈 문자열 반환

        # n. 실제 클립보드 내용인 stdout_lines (리스트)를 줄바꿈 문자로 합쳐서 반환합니다.
        return "\n".join(stdout_lines)
    else:
        try:
            import clipboard
            logging.debug("way3 : clipboard.paste()")
            return clipboard.paste()
        except ImportError:
            # clipboard 모듈이 없는 경우 빈 문자열 반환
            return ""
def get_process_name_by_pid(pid):
    import logging
    try:
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

        data = ensure_command_executed(cmd=f'tasklist | findstr "{pid}"')
        # ensure_command_executed returns (stdout_lines, stderr_lines)
        stdout_lines = data[0]
        if stdout_lines and len(stdout_lines) > 0:
            # Assuming the first line contains the process name
            process_info_line = stdout_lines[0]
            # Split the line to get the process name (first part)
            process_name = process_info_line.split(" ")[0]
            return process_name
        else:
            logging.debug(rf"process_name of pid {pid} not found")
            return None

    except Exception as e:
        logging.debug(f"프로세스명 검색 중 오류 발생: {e}")
        return None
def get_process_info_by_process_name(process_name):
    import psutil

    process_name_lower = process_name.lower()
    found_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc_name = proc.info['name'].lower()
            if process_name_lower in proc_name or proc_name in process_name_lower:
                found_processes.append((
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['exe']
                ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return found_processes
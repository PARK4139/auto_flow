import psutil
def get_process_info_by_pid(pid):
    try:
        process = psutil.Process(pid)
        return (pid, process.name(), process.exe())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def command_exists(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None

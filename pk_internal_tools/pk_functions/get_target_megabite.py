def get_target_megabite(target_path):
    return get_target_bite(target_path.strip()) / 1024 ** 2

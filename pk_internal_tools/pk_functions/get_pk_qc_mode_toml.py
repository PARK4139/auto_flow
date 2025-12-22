import logging


def get_pk_qc_mode_toml(key: str, initial: str) -> str:
    import os
    from pk_internal_tools.pk_objects.pk_directories import D_PK_TOKENS

    path = D_PK_TOKENS / f"pk_token_{key}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(initial)
        logging.debug(f"[Config] Initialized '{key}' with default '{initial}' in {path}")
        return initial
    with open(path, 'r', encoding='utf-8') as f:
        value = f.readline().strip() or initial
    logging.debug(f"[Config] Loaded '{key}' = '{value}'")
    return value

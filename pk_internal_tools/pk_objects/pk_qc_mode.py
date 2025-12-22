import json
from pathlib import Path


def _get_qc_mode_status_file_path() -> Path:
    from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
    return Path(D_PK_CONFIG) / "qc_mode_status.json"


def _get_qc_mode_status() -> bool:
    qc_mode_file = _get_qc_mode_status_file_path()
    if not qc_mode_file.exists():
        return False
    try:
        with open(qc_mode_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("qc_mode", False)
    except (json.JSONDecodeError, FileNotFoundError):
        return False


QC_MODE = _get_qc_mode_status()

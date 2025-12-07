from __future__ import annotations

from pathlib import Path
from typing import Union

import logging
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_script_file_created(
        script_file: Union[str, Path],
        script_content: str,
        mode: str = "w",
        encoding: str = "utf-8",
        ensure_parent: bool = True,
        force_crlf: bool = True,
        add_bom_for_utf8: bool = False,
) -> Path:

    import os
    from pathlib import Path

    # Normalize and expand the path
    p = Path(script_file) if isinstance(script_file, (str, Path)) else Path(str(script_file))
    p = Path(os.path.expandvars(os.path.expanduser(str(p))))

    # Ensure parent directory
    if ensure_parent:
        p.parent.mkdir(parents=True, exist_ok=True)

    # Normalize newlines for batch files if requested
    content = script_content
    if force_crlf:
        # Convert any newline style to CRLF
        content = content.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")

    # Decide final encoding
    final_encoding = "utf-8-sig" if add_bom_for_utf8 or encoding.lower() == "utf-8-sig" else encoding

    # Write the file; newline="" to preserve our CRLF
    with p.open(mode=mode, encoding=final_encoding, newline="") as f:
        f.write(content)

    # Verify
    if not p.exists():
        logging.debug(f"File not created: {p}")
        raise FileNotFoundError(f"File not created: {p}")
    if p.stat().st_size == 0:
        logging.debug(f"File is empty after write: {p}")
        raise IOError(f"File is empty after write: {p}")
    return p

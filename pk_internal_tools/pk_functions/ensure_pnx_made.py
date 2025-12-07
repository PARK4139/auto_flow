def ensure_pnx_made(pnx, mode):
    from pathlib import Path
    import logging

    path = Path(pnx)
    if mode == "f":
        # ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            try:
                path.touch()
            except Exception as e:
                logging.error(f"Failed to create file {path}: {e}")
                raise
    elif mode == "d":
        path.mkdir(parents=True, exist_ok=True)
    else:
        logging.error("❌ ensure_pnx_made: mode must be 'f' or 'd'")
        return

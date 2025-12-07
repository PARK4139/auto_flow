def ensure_pnx_normalized_this_file(prefixes=('D_', 'F_')):
    from pathlib import Path
    for k, v in list(globals().items()):
        if any(k.startswith(prefix) for prefix in prefixes) and isinstance(v, str):
            try:
                new_path = None
                try:
                    from pathlib import Path
                    new_path = Path(v)
                except:
                    if isinstance(v, Path):
                        return v
                    elif isinstance(v, str):
                        v = str(Path(v))
                globals()[k] = new_path
                print(f"[정규화] {k}: {v} -> {new_path}")
            except Exception as e:
                print(f"[스킵] {k}: {e}")

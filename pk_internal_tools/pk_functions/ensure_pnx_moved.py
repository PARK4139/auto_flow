def ensure_pnx_moved(pnx, d_dst, with_overwrite=False, sequential_mode=False, timestamp_mode=True):
    import logging
    import shutil
    import traceback
    from datetime import datetime
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.is_d import is_d
    from pk_internal_tools.pk_functions.is_f import is_f
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    pnx = Path(pnx)
    d_dst = Path(d_dst)
    d_dst.mkdir(parents=True, exist_ok=True)

    def _gen_sequential(dst_dir: Path, base_name: str, ext: str) -> Path:
        for i in range(1, 1000):
            c = dst_dir / f"{base_name}_seq({i})_{ext}"
            if not c.exists():
                return c
        raise RuntimeError("Too many duplicates to resolve with sequential mode.")

    def _gen_timestamped(dst_dir: Path, base_name: str, ext: str) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        return dst_dir / f"{base_name}_ts({ts})_{ext}"

    def _force_overwrite_move(src: Path, dst: Path) -> Path:
        """
        Overwrite `dst` (file or dir) then move `src` -> `dst`.
        Ensures parent exists. Works for both files and directories.
        """
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            if dst.exists():
                if dst.is_dir():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()
            shutil.move(str(src), str(dst))
            logging.debug(f"[OVERWRITE MOVE] '{src}' → '{dst}'")
            return dst
        except Exception as e:
            logging.warning(f"Failed to move with overwrite: {e}")
            return None

    try:
        # Sanity checks
        if not pnx.exists():
            logging.warning(f"[{PkTexts.NOT_FOUND}] Source does not exist: '{pnx}'")
            return None

        src_type = 'f' if is_f(pnx) else 'd' if is_d(pnx) else 'unknown'

        # --- OVERWRITE MODE ---
        if with_overwrite is True:
            # If d_dst is an existing directory -> move under it using original name
            if d_dst.exists() and d_dst.is_dir():
                dst = d_dst / get_nx(pnx)
                result = _force_overwrite_move(pnx, dst)
            else:
                # d_dst is treated as the final path (file or dir name included)
                result = _force_overwrite_move(pnx, d_dst)

            if result is not None:
                if QC_MODE:
                    logging.debug(
                        f"src_type={src_type} dst_pnx={str(result):<150} "
                        f"dst_dir={str(result.parent):<50}  "
                    )
                else:
                    logging.debug(f"[MOVE] '{pnx}' → '{result}'")
            return result

        # --- NON-OVERWRITE MODE ---
        # Always treat d_dst as a directory destination here.
        dst_dir = d_dst
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / get_nx(pnx)

        if dst.exists():
            base_name = dst.stem
            ext = dst.suffix

            if timestamp_mode:
                dst = _gen_timestamped(dst_dir, base_name, ext)
            elif sequential_mode:
                dst = _gen_sequential(dst_dir, base_name, ext)
            else:
                logging.debug(f"[{PkTexts.ALREADY_EXIST}] '{dst}' (skip)")
                return None

        shutil.move(str(pnx), str(dst))

        if QC_MODE:
            logging.debug(
                f"src_type={src_type} dst_pnx={str(dst):<150} "
                f"dst_dir={str(dst_dir):<50}  "
            )
        else:
            logging.debug(f"[MOVE] '{pnx}' → '{dst}'")
        return dst

    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        return None

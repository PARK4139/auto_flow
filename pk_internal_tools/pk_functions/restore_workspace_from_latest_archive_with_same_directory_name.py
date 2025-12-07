

def restore_workspace_from_latest_archive_with_same_directory_name(D_PKG_ARCHIVED, d_working):
    archives = sorted(
        [f for f in os.listdir(D_PKG_ARCHIVED) if f.endswith('.tar.bz2')],
        key=lambda f: os.path.getmtime(os.path.join(D_PKG_ARCHIVED, f)),
        reverse=True
    )
    if not archives:
        logging.warning(f"[{PkTexts.ERROR}] No backup archive found in {D_PKG_ARCHIVED}")
        return

    latest_archive = os.path.join(D_PKG_ARCHIVED, archives[0])
    logging.debug(f"[{PkTexts.REVERT}] Restoring from {latest_archive}")

    if os.path.exists(d_working):
        shutil.rmtree(d_working)

    os.makedirs(d_working, exist_ok=True)
    with tarfile.open(latest_archive, "r:bz2") as tar:
        tar.extractall(path=d_working)

    logging.debug(f"[{PkTexts.REVERT}] Restored to {d_working}")


